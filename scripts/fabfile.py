#!/usr/bin/env python

import json
import datetime
from os.path import expanduser
from fabric.api import env, run, settings, local, roles, cd, prefix
from fabric.contrib.files import exists

"""
    fab integration git_export
    fab integration deploy
"""

env.project_name = 'gotgame'

env.export_path = '/tmp/export/%(project_name)s/latest/' % env

env.deploy_dir = '/srv/%(project_name)s' % env
env.virtualenv_path = '%(deploy_dir)s/env' % env
env.user = 'ubuntu'
env.key_filename = '%s/.ssh/gg.pem' % expanduser("~")

fab_project_root = '../'


def git_export():
    with settings(warn_only=True):
        local('rm -rf %(export_path)s' % env)
    local('mkdir -p %(export_path)s' % env)

    local(
            'cd ../ && git archive --format=tar ' +
            '%(branch)s | tar -x -C %(export_path)s' % env
        )


def deploy():
    update_code()

    with prefix('source %(virtualenv_path)s/bin/activate' % env):
        collect_static()
        update_virtualenv()
        migrate_db()
        repoint_symlink()
        restart_gunicorn()


@roles('web')
def update_code():
    env.deploy_date = datetime.datetime.now().strftime(
            '%Y-%m-%d-%H%M%S'
        )
    env.deploy_path = '%(deploy_dir)s/%(deploy_date)s' % env

    run('mkdir -p %(deploy_path)s' % env)

    if exists('%(deploy_dir)s/current' % env):
        env.rsync_link_dest = '--link-dest %(deploy_dir)s/current' % env
    else:
        env.rsync_link_dest = ''
    local("rsync -e 'ssh -i %(key_filename)s' %(export_path)s %(user)s@%(host_string)s:%(deploy_path)s %(rsync_link_dest)s --recursive --delete" % env)

    with cd('%(deploy_path)s' % env):
        # putting test settings into place
        run('cp %(project_name)s/settings/%(env_name)s.py %(project_name)s/settings/local.py' % env)

        # putting env_values into place
        run('cp %(deploy_dir)s/configs/%(env_name)s_env_values.py %(project_name)s/settings/env_values.py' % env)

        # change permissions
        run('chmod ug+x gunicorn.sh')


@roles('web')
def migrate_db():
    with cd('%(deploy_path)s' % env):
        run('%(virtualenv_path)s/bin/python manage.py syncdb --noinput' % env)
        run('%(virtualenv_path)s/bin/python manage.py migrate' % env)


@roles('web')
def update_virtualenv():
    if not exists('%(virtualenv_path)s' % env):
        run('virtualenv --no-site-packages %(virtualenv_path)s' % env)

    with cd('%(deploy_path)s' % env):
        run('%(virtualenv_path)s/bin/pip install -r requirements/%(env_name)s.txt --use-mirrors' % env)


@roles('web')
def repoint_symlink():
    # repointing current and previous
    with settings(warn_only=True):
        run('rm %(deploy_dir)s/previous' % env)
        run('mv %(deploy_dir)s/current %(deploy_dir)s/previous' % env)
    run('ln -s %(deploy_path)s %(deploy_dir)s/current' % env)

    # removing old folders
    with cd('%(deploy_dir)s' % env):
        run('rm -rf `find . -maxdepth 1 -type d | grep "^\./20" | sort -r | sed  \'1,5d\'`')


@roles('web')
def collect_static():
    with cd('%(deploy_path)s' % env):
        run('%(virtualenv_path)s/bin/python manage.py collectstatic --noinput' % env)

@roles('web')
def rollback():
    run('mv %(deploy_dir)s/current %(deploy_dir)s/_previous' % env)
    run('mv %(deploy_dir)s/previous %(deploy_dir)s/current' % env)
    run('mv %(deploy_dir)s/_previous %(deploy_dir)s/previous' % env)


@roles('web')
def restart_gunicorn():
    run('sudo supervisorctl restart %(project_name)s' % env)

def environment(env_name):
    env.env_name = env_name

    _js = json.load(open('environments.json'))
    env_def = _js[env_name]
    env.roledefs = env_def['roles']

    env.hosts = []
    for role_name, hosts in env.roledefs.items():
        env.hosts = env.hosts + hosts

    env.branch = env_def['branch']


def integration():
    environment('integration')

#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn/gotgame.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=ubuntu
GROUP=ubuntu
ADDRESS=127.0.0.1:8000
cd /srv/gotgame/current
source /srv/gotgame/env/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn gotgame.wsgi:application -w $NUM_WORKERS --bind=$ADDRESS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE 2>>$LOGFILE

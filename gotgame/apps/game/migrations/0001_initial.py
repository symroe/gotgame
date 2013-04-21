# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'game_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('credits', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'game', ['Profile'])

        # Adding model 'Banked'
        db.create_table(u'game_banked', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Profile'])),
            ('credits', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'game', ['Banked'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'game_profile')

        # Deleting model 'Banked'
        db.delete_table(u'game_banked')


    models = {
        u'game.banked': {
            'Meta': {'object_name': 'Banked'},
            'credits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Profile']"})
        },
        u'game.profile': {
            'Meta': {'object_name': 'Profile'},
            'credits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['game']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Banked.created'
        db.add_column(u'game_banked', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Banked.modified'
        db.add_column(u'game_banked', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Profile.created'
        db.add_column(u'game_profile', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Profile.modified'
        db.add_column(u'game_profile', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Banked.created'
        db.delete_column(u'game_banked', 'created')

        # Deleting field 'Banked.modified'
        db.delete_column(u'game_banked', 'modified')

        # Deleting field 'Profile.created'
        db.delete_column(u'game_profile', 'created')

        # Deleting field 'Profile.modified'
        db.delete_column(u'game_profile', 'modified')


    models = {
        u'game.banked': {
            'Meta': {'object_name': 'Banked'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'credits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Profile']"})
        },
        u'game.profile': {
            'Meta': {'object_name': 'Profile'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'credits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['game']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SearchGroup'
        db.create_table(u'srm_search_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group_name', self.gf('django.db.models.fields.CharField')(default=u'new group', max_length=100)),
            ('top_level_domain', self.gf('django.db.models.fields.CharField')(default=u'com', max_length=20)),
            ('lang', self.gf('django.db.models.fields.CharField')(default=u'en', max_length=2)),
            ('results_per_page', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('results_cnt', self.gf('django.db.models.fields.IntegerField')(default=100)),
        ))
        db.send_create_signal(u'srm_model', ['SearchGroup'])

        # Adding model 'Keywords'
        db.create_table(u'srm_keywords', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('search_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['srm_model.SearchGroup'])),
        ))
        db.send_create_signal(u'srm_model', ['Keywords'])

        # Adding model 'Website'
        db.create_table(u'srm_website', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'', max_length=250, blank=True)),
            ('search_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['srm_model.SearchGroup'])),
        ))
        db.send_create_signal(u'srm_model', ['Website'])

        # Adding model 'WebsiteRank'
        db.create_table(u'srm_website_rank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rank_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('search_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['srm_model.SearchGroup'])),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['srm_model.Website'])),
            ('website_pos', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'srm_model', ['WebsiteRank'])


    def backwards(self, orm):
        # Deleting model 'SearchGroup'
        db.delete_table(u'srm_search_group')

        # Deleting model 'Keywords'
        db.delete_table(u'srm_keywords')

        # Deleting model 'Website'
        db.delete_table(u'srm_website')

        # Deleting model 'WebsiteRank'
        db.delete_table(u'srm_website_rank')


    models = {
        u'srm_model.keywords': {
            'Meta': {'object_name': 'Keywords', 'db_table': "u'srm_keywords'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'search_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srm_model.SearchGroup']"})
        },
        u'srm_model.searchgroup': {
            'Meta': {'object_name': 'SearchGroup', 'db_table': "u'srm_search_group'"},
            'group_name': ('django.db.models.fields.CharField', [], {'default': "u'new group'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "u'en'", 'max_length': '2'}),
            'results_cnt': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'results_per_page': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'top_level_domain': ('django.db.models.fields.CharField', [], {'default': "u'com'", 'max_length': '20'})
        },
        u'srm_model.website': {
            'Meta': {'object_name': 'Website', 'db_table': "u'srm_website'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srm_model.SearchGroup']"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '250', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'srm_model.websiterank': {
            'Meta': {'object_name': 'WebsiteRank', 'db_table': "u'srm_website_rank'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank_date': ('django.db.models.fields.DateTimeField', [], {}),
            'search_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srm_model.SearchGroup']"}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srm_model.Website']"}),
            'website_pos': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['srm_model']
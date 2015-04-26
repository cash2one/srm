# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'SearchGroup', fields ['group_name']
        db.create_unique(u'srm_search_group', ['group_name'])

        # Adding field 'WebsiteRank.keywords'
        db.add_column(u'srm_website_rank', 'keywords',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['srm_model.Keywords'], null=True),
                      keep_default=False)

        # Adding unique constraint on 'WebsiteRank', fields ['rank_date', 'search_group', 'website', 'keywords']
        db.create_unique(u'srm_website_rank', ['rank_date', 'search_group_id', 'website_id', 'keywords_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'WebsiteRank', fields ['rank_date', 'search_group', 'website', 'keywords']
        db.delete_unique(u'srm_website_rank', ['rank_date', 'search_group_id', 'website_id', 'keywords_id'])

        # Removing unique constraint on 'SearchGroup', fields ['group_name']
        db.delete_unique(u'srm_search_group', ['group_name'])

        # Deleting field 'WebsiteRank.keywords'
        db.delete_column(u'srm_website_rank', 'keywords_id')


    models = {
        u'srm_model.keywords': {
            'Meta': {'object_name': 'Keywords', 'db_table': "u'srm_keywords'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'search_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srm_model.SearchGroup']"})
        },
        u'srm_model.searchgroup': {
            'Meta': {'object_name': 'SearchGroup', 'db_table': "u'srm_search_group'"},
            'group_name': ('django.db.models.fields.CharField', [], {'default': "u'new group'", 'unique': 'True', 'max_length': '100'}),
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
            'Meta': {'unique_together': "((u'rank_date', u'search_group', u'website', u'keywords'),)", 'object_name': 'WebsiteRank', 'db_table': "u'srm_website_rank'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srm_model.Keywords']", 'null': 'True'}),
            'rank_date': ('django.db.models.fields.DateTimeField', [], {}),
            'search_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srm_model.SearchGroup']"}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['srm_model.Website']"}),
            'website_pos': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['srm_model']
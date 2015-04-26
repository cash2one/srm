# -*- coding: utf-8 -*-

# TODO: Also note: You'll have to insert the output of 'django-admin.py sqllcustom [appname]' into your database.
# from __future__ import unicode_literals
from django.db import models
from django.db.models.loading import get_model

# d:\PycharmProjects\srm>python manage.py schemamigration srm_model --auto --settings=srm.settings
# d:\PycharmProjects\srm>python manage.py migrate srm_model --settings=srm.settings


class SearchGroup(models.Model):
    group_name = models.CharField(max_length=100, default='new group', unique=True)
    top_level_domain = models.CharField(max_length=20, default='com')
    lang = models.CharField(max_length=2, default='en')
    results_per_page = models.IntegerField(default=10)
    results_cnt = models.IntegerField(default=100)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'srm_search_group'


class Keywords(models.Model):
    keywords = models.CharField(max_length=500)
    search_group = models.ForeignKey(SearchGroup)

    def __str__(self):
        return self.keywords

    class Meta:
        db_table = 'srm_keywords'


class Website(models.Model):
    url = models.CharField(max_length=250)
    title = models.CharField(max_length=250, blank=True, default='')
    search_group = models.ForeignKey(SearchGroup)
#    squery = models.ManyToManyField(Squery, through='SqueryWebsiteMm')

    def __str__(self):
        return self.url

    class Meta:
        db_table = 'srm_website'


class WebsiteRank(models.Model):
    rank_date = models.DateTimeField()
    search_group = models.ForeignKey(SearchGroup)
    website = models.ForeignKey(Website)
    keywords = models.ForeignKey(Keywords)
    website_pos = models.IntegerField(default=0)

    def __str__(self):
        return 'id: ' + str(self.id) + ' ' + 'position: ' + str(self.website_pos)

    class Meta:
        db_table = 'srm_website_rank'
        unique_together = ('rank_date', 'search_group', 'website', 'keywords',)


# def create_WebsiteRank():
#     # class WebsiteRank(models.Model):
#     #     rank_date = models.DateTimeField()
#     #     search_group = models.ForeignKey(SearchGroup)
#     #     website = models.ForeignKey(Website)
#     #     keywords = models.ForeignKey(Keywords)
#     #     website_pos = models.IntegerField(default=0)
#     #
#     #     def __str__(self):
#     #         return 'id: ' + str(self.id) + ' ' + 'position: ' + str(self.website_pos)
#     #
#     #     class Meta:
#     #         db_table = 'srm_website_rank'
#     #         unique_together = ('rank_date', 'search_group', 'website', 'keywords',)
#     #
#     # m = get_model(u'srm_model', 'WebsiteRank', seed_cache=False, only_installed=False)
#     # m.add_to_class('website_pos', models.IntegerField(default=0))
#
#     class Meta:
#         db_table = 'srm_website_rank'
#         unique_together = ('rank_date', 'search_group', 'website', 'keywords',)
#
#     module = 'srm_model.models'
#     attrs = {'__module__': module,
#             'Meta': Meta,
#             'rank_date': models.DateTimeField(),
#             'search_group': models.ForeignKey(SearchGroup),
#             'website': models.ForeignKey(Website),
#             'keywords': models.ForeignKey(Keywords),
#             'website_pos': models.IntegerField(default=0),
#             'rank_date': models.DateTimeField(),
#     }
#
#
#     cls = type('WebsiteRank', (models.Model,), attrs)
#     m = get_model(u'srm_model', 'WebsiteRank', seed_cache=False, only_installed=False)
#
#
# create_WebsiteRank()

#############################################################################################






# class Squery(models.Model):
#     top_level_domain = models.CharField(max_length=20, default='com')
#     lang = models.CharField(max_length=2, default='en')
#     results_per_page = models.IntegerField(default=10)
#     results_cnt = models.IntegerField(default=100)
#     keywords = models.CharField(max_length=250)
#
#     def __str__(self):
#         return self.keywords
#
#     class Meta:
#         db_table = 'squery'
#
#
# class Website(models.Model):
#     url = models.CharField(max_length=250)
#     title = models.CharField(max_length=250, blank=True, default='')
#     squery = models.ManyToManyField(Squery, through='SqueryWebsiteMm')
#
#     def __str__(self):
#         return self.url
#
#     class Meta:
#         db_table = 'website'
#
#
# class SqueryWebsiteMm(models.Model):
#     squery = models.ForeignKey(Squery)
#     website = models.ForeignKey(Website)
#
#     def __str__(self):
#         return 'squery_id: ' + str(self.squery) + '; ' + 'website_id: ' + str(self.website)
#
#     class Meta:
#         db_table = 'squery_website_mm'
#
#
# class WebsiteRank(models.Model):
#     rank_date = models.DateTimeField()
#     squery_website_mm = models.ForeignKey(SqueryWebsiteMm)
#     website_pos = models.IntegerField(default=0)
#
#     def __str__(self):
#         return 'id: ' + str(self.id) + ' ' + 'position: ' + str(self.website_pos)
#
#     class Meta:
#         db_table = 'website_rank'
#
#
#

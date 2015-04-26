# -*- coding: utf-8 -*-

from django.db import connection
from datetime import date, timedelta

RANK_CHANGES_TXT = """
  SELECT G.id AS group_id,
    K.id AS keywords_id,
    W.id AS website_id,
    G.group_name,
    W.url,
    W.title,
    K.keywords,
    %s AS date1,
    (
      SELECT website_pos
        FROM srm_website_rank
        WHERE rank_date = date1
          AND search_group_id = G.id
          AND website_id = W.id
          AND keywords_id = K.id
    ) AS pos1,
    %s AS date2,
    (
      SELECT website_pos
        FROM srm_website_rank
        WHERE rank_date = date2
          AND search_group_id = G.id
          AND website_id = W.id
          AND keywords_id = K.id
    ) AS pos2,
	G.results_per_page AS res_cnt
   FROM srm_search_group G
    INNER JOIN srm_keywords K
      ON K.search_group_id = G.id
    INNER JOIN srm_website W
      ON W.search_group_id = G.id
  ORDER BY G.group_name, W.title, K.keywords
"""


def rank_changes_sql(rank_date1, rank_date2):
    """ returns list of ordered by (group_name, title, keywords) rows which looks like:
            { 'date1': u'2014-06-04',
              'date2': u'2014-06-03',
              'group_id': 39L,
              'group_name': u'Aroundafricasafari',
              'keywords': u'Africa Safaris',
              'keywords_id': 257L,
              'pos1': None,
              'pos2': None,
              'title': u'Aroundafricasafari.com',
              'url': u'http://aroundafricasafari.com',
              'website_id': 38L
               'res_cnt' : 10
            },...
    """

    cursor = connection.cursor()
    cursor.execute(RANK_CHANGES_TXT, [rank_date1, rank_date2,])
    rs = cursor.fetchall()
    fields_lst = get_field_names(cursor)
    named_row_lst = [row_to_dic(row, fields_lst) for row in rs]
    return named_row_lst


def get_field_names(cursor):
    return [col[0] for col in cursor.description]


def row_to_dic(row, field_names):
    return dict(zip(field_names, row))

if __name__ == '__main__':
    date1 = date.today()
    date2 = (date1 - timedelta(days=1))
    print rank_changes_sql(date1, date2)
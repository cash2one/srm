#!/usr/bin/python
# -*- coding: utf-8 -*-

from MySQLdb import connect
from setuptools.command.rotate import rotate
from srm.settings import DB_PARMS
#import query_samples as qs
from search_query import find_rank
import datetime
from email_sending import send_ranking_report
from random import randint
import logging
from html_storage import create_html_folder

def update_ranks():
    logging.info('')
    logging.info('START GOOGLE SCRAPING %s', datetime.datetime.now().strftime('%b %d, %Y, %I:%M:%S:%f %p'))
    logging.info('')
    cur_date = datetime.date.today()
    create_html_folder()
    for search_query, website_lst in search_query_iter():
        for site_rank in find_rank(search_query, website_lst):
            save_rank(site_rank, cur_date)

    send_ranking_report(cur_date)
    logging.info('')
    logging.info('STOP GOOGLE SCRAPING %s', datetime.datetime.now().strftime('%b %d, %Y, %I:%M:%S:%f %p'))
    logging.info('')


def save_rank(site_rank, rank_date):
    """ site_rank is a dictionary of:
    {group_id, website_id, keywords_id, site_pos}
    """
    if not isinstance(rank_date, datetime.date):
            raise TypeError("rank_date must be a datetime.date type")
    db = connect_to_db()
    website_rank_cur = db.cursor()

    website_rank_cur.execute("""SELECT R.id
                                FROM srm_website_rank R
                                WHERE rank_date = %s AND search_group_id = %s AND website_id = %s AND keywords_id = %s;
                                """,
                    (rank_date,
                     site_rank['group_id'],
                     site_rank['website_id'],
                     site_rank['keywords_id'],))

    rows = website_rank_cur.fetchall()
    if len(rows) == 1:
        website_rank_id = rows[0][0]
        website_rank_cur.execute("""UPDATE srm_website_rank
                      SET website_pos = %s
                      WHERE id = %s
                    """,
                    (site_rank['site_pos'], website_rank_id,))
    elif len(rows) == 0:
        website_rank_cur.execute("""INSERT INTO srm_website_rank
                          (rank_date, website_pos, search_group_id, website_id, keywords_id)
                          VALUES(%s, %s, %s, %s, %s);
                    """,
                    (rank_date,
                     site_rank['site_pos'],
                     site_rank['group_id'],
                     site_rank['website_id'],
                     site_rank['keywords_id']))
    else:
        pass
    db.commit()
    db.close()


def search_query_iter():
    db = connect_to_db()
    sq_cursor = db.cursor()
    sq_cursor.execute(
        """SELECT G.id AS group_id,
                G.group_name,
                G.top_level_domain AS tld,
                G.lang,
                G.results_per_page,
                G.results_cnt,
                K.id AS keywords_id,
                K.keywords
            FROM srm_search_group G
                JOIN srm_keywords K
                    ON G.id = K.search_group_id;
        """
    )
    sq_field_names = get_field_names(sq_cursor)
    rs = [item for item in sq_cursor.fetchall()]
    sq_cursor.close()
    while True:
        if len(rs) == 0:
            break
        row_num = randint(0, len(rs) - 1)
        row = rs[row_num]
        del rs[row_num]
        #print len(rs), row_num
        sq_record = row_to_dic(row, sq_field_names)
        # print '___________________________________'
        #print sq_record
        website_cur = db.cursor()
        website_cur.execute(
            """SELECT W.id AS website_id,
                    W.url,
                    W.title,
                    W.search_group_id AS group_id
                FROM srm_website W
                WHERE W.search_group_id = %s;
            """, (sq_record['group_id'],)
        )
        website_rs = website_cur.fetchall()
        website_fields = get_field_names(website_cur)
        website_cur.close()
        website_lst = [row_to_dic(site, website_fields) for site in website_rs]
        yield sq_record, website_lst

    db.close()


def get_field_names(cursor):
    return [col[0] for col in cursor.description]


def row_to_dic(row, field_names):
    return dict(zip(field_names, row))


def connect_to_db():
    return connect(**DB_PARMS)


if __name__ == '__main__':
    logging.basicConfig(filename='rank_monitor.log', level=logging.INFO)
    update_ranks()

# TODO: save current state. Restore it if something has been failed
# TODO: add proxy
# TODO: insert random stab search queries between real queries
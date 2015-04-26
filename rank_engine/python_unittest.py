#!/usr/bin/python
#-*- coding: utf-8 -*-

import unittest
import datetime
import random
from rank_monitor import search_query_iter
from srm_model.data_samples import search_group_samples
from rank_engine.rank_monitor import connect_to_db
from srm_model.data_samples import write_website_tbl, write_keywords_tbl, write_search_group_tbl
from rank_monitor import save_rank


class RankMonitorTest(unittest.TestCase):
    def test_save_rank(self):
        group_id, website_id, keywords_id = self.create_test_group()
        rank_date = datetime.date.today()
        pos = 20
        id_lst = self.get_position_id(group_id, website_id, keywords_id, rank_date)
        if id_lst is not None:
            self.assertEqual(len(id_lst), 0, 'Group %d already has positions' % (group_id,))
        rank = {'group_id': group_id, 'website_id': website_id, 'keywords_id': keywords_id, 'site_pos': pos}
        save_rank(rank, rank_date)
        id2_lst = self.get_position_id(group_id, website_id, keywords_id, rank_date)
        self.assertIsNotNone(id2_lst, 'Group %d must have rank' % (group_id,))
        self.assertEqual(len(id2_lst), 1, 'Group %d has positions count %d' % (group_id, len(id2_lst)))

        self.delete_position(id2_lst[0][0])

    def create_test_group(self):
        db = connect_to_db()
        cur = db.cursor()
        group_name = self.get_random_name()
        group_id = write_search_group_tbl(cur, group_name, 'com', 'en', 100)
        website_id = write_website_tbl(cur, group_id, 'test site', 'test site')
        keywords_id = write_keywords_tbl(cur, group_id, 'test keywords')
        db.commit()
        db.close()
        return group_id, website_id, keywords_id

    def get_random_name(self):
        r_name = 'test_group_%d' % (random.randint(1, 1000000),)
        return r_name

    def delete_test_group(self, group_id, website_id, keywords_id):
        db = connect_to_db()
        cur = db.cursor()
        cur.execute("""DELETE FROM srm_website WHERE id = %s; """ %(website_id,))
        cur.execute("""DELETE FROM srm_keywords WHERE id = %s; """ %(keywords_id,))
        cur.execute("""DELETE FROM srm_search_group WHERE id = %s; """ %(group_id,))
        db.commit()
        db.close()

    def get_position_id(self, group_id, website_id, keywords_id, rank_date):
        db = connect_to_db()
        cur = db.cursor()
        cur.execute("""SELECT R.id
                        FROM srm_website_rank R
                        WHERE rank_date = %s AND search_group_id = %s AND website_id = %s AND keywords_id = %s;
                        """,
                    (rank_date,
                     group_id,
                     website_id,
                     keywords_id)
        )
        rows = cur.fetchall()
        db.commit()
        db.close()
        return rows

    def check_position(self, website_rank_id, site_pos):
        db = connect_to_db()
        cur = db.cursor()
        cur.execute("""SELECT R.website_pos
                        FROM srm_website_rank R
                        WHERE R.id = %s;
                        """,
                    (website_rank_id,)
        )
        row = cur.fetchone()
        db.commit()
        db.close()
        test_pos = row[0]
        self.assertEqual(test_pos, site_pos, 'Wrong site position %d' % (test_pos,))

    def delete_position(self, website_rank_id):
        db = connect_to_db()
        cur = db.cursor()
        cur.execute("""DELETE FROM srm_website_rank WHERE id = %s; """ %(website_rank_id,))
        db.commit()
        db.close()

    def test_search_query_iter(self):
        print 'Test rank_monitor.search_query_iter'
        search_groups = {}
        for search_query, website_lst in search_query_iter():
            self.check_sq_scheme(search_query)
            for website in website_lst:
                self.check_website_scheme(website)
            group_name = search_query['group_name']
            if group_name not in search_groups:
                search_groups[group_name] = {
                    'lang': search_query['lang'],
                    'results_cnt': search_query['results_cnt'],
                    'results_per_page': search_query['results_per_page'],
                    'tld': search_query['tld'],
                    'site_lst': [{'url': website['url'], 'title': website['title']} for website in website_lst],
                    'keywords_lst': [{'keywords': search_query['keywords']}, ]
                }
            else:
                for website in website_lst:
                    dic1 = {'url': website['url'], 'title': website['title']}
                    for dic2 in search_groups[group_name]['site_lst']:
                        if dic1 == dic2:
                            break
                    else:  #append only new records
                        search_groups[group_name]['site_lst'].append(dic1)

                search_groups[group_name]['keywords_lst'].append({'keywords': search_query['keywords']})

        self.compare_all_groups(search_group_samples, search_groups)

    def compare_all_groups(self, search_groups, test_search_groups):
        names1 = set(search_groups.keys())
        names2 = set(test_search_groups.keys())
        self.assertEqual(names1, names2, 'Group names in data samples and test data are not equal')
        for group_name, val in search_groups.items():
            self.compare_group(val, test_search_groups[group_name])

    def compare_group(self, group, test_group):
        #test group can have additional attributes
        for elem_name, elem_val in group.items():
            if type(elem_val) is tuple or type(elem_val) is list:
                self.assertEqual(
                    set((tuple(sorted(d.items())) for d in elem_val)),
                    set((tuple(sorted(d.items())) for d in test_group[elem_name])),
                    'List of websites or keywords are not equal'
                )
            else:
                self.assertEqual(elem_val, test_group[elem_name])

    def check_sq_scheme(self, search_query):
        names = set(['group_id',
                     'group_name',
                     'tld',
                     'lang',
                     'results_per_page',
                     'results_cnt',
                     'keywords_id',
                     'keywords']
        )
        self.assertEqual(set(search_query.keys()),
                         names,
                         'Wrong search query dictionary names')

    def check_website_scheme(self, website):
        self.assertEqual(set(website.keys()),
                         set(['website_id', 'url', 'title', 'group_id']),
                         'Wrong website dictionary names')



# class GQueryTest(unittest.TestCase):
#     def test_google_page_links(self):
#         print 'test_google_page_links'
#         for query_dic in qs_lst:
#             query_txt = query_dic['query_txt']  #query text
#             pages_cnt = query_dic['pages_cnt']
#             links_per_page = query_dic['links_per_page']
#             print '-------------------------------------------------------------------------'
#             print 'QUERY:', query_txt, '  Pages count:', pages_cnt, '  Links per page:', links_per_page
#
#             g_query = create_squery(query_txt)
#             page_links_iter = result_links_iter(g_query)
#             last_page_num = 0
#             page_link_cnt = links_per_page
#             for url, page_num, pos_in_page in page_links_iter:
#                 print 'page_num:', page_num, 'pos_in_page:', pos_in_page, 'url:', url
#                 if last_page_num != page_num:
#                     self.assertEqual(last_page_num + 1, page_num, 'Order of pages is wrong %d, %d' %
#                                                                   (last_page_num, page_num))
#                     last_page_num += 1
#
#                 if pos_in_page == 1:
#                     self.assertEqual(page_link_cnt, links_per_page, 'Incorrect links count %d for page %d'
#                                                                     % (page_link_cnt, last_page_num))
#                     page_link_cnt = 1
#                 else:
#                     page_link_cnt += 1
#                     self.assertEqual(page_link_cnt, pos_in_page,
#                                      'Incorrect links order %d, %d ' % (page_link_cnt, pos_in_page))
#
#                 match_obj = match(url)
#                 self.assertIsNotNone(match_obj, 'Wrong url "%s"' % url)
#
#             self.assertEqual(last_page_num, pages_cnt, 'Wrong pages number %d' % last_page_num)
#
#     def test_find_rank(self):
#         for query_txt, page_lst in query_site_rank_tree().iteritems():
#             g_query = create_squery(query_txt)
#             page_rank_lst = [create_site_rank_dic(website_id=get_website_id(page['url_txt']),
#                                                   site_url=page['url_txt'],
#                                                   squery_id=get_query_id(query_txt),
#                                                   keywords=query_txt) for page in page_lst]
#
#             for page_rank in find_rank(g_query, page_rank_lst):
#                 self.assertTrue(self.check_page_rank(page_rank, page_lst))
#
#     def check_page_rank(self, page_rank, page_lst):
#         for page in page_lst:
#             if page_rank['url'] == page['url_txt']:
#                 if page_rank['page_num'] == page['page_num'] and \
#                                 page_rank['pos_in_page'] == page['pos_in_page']:
#                     return True
#                 else:
#                     return False
#         else:
#             raise ItemNotFoundError('Page url \'%s\' was not found in pages list' % page_rank['url_txt'])
#

if __name__ == '__main__':
    unittest.main()
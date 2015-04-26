# -*- coding: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
# from django.test import TestCase
# from query_samples import squery_samples_lst as qs_lst, query_site_rank_tree, get_website_id, get_query_id, \
#     ItemNotFoundError
# from search_query import create_squery, create_site_rank_dic, result_links_iter, find_rank
# from rfc3987 import match
#
#
# class SQueryTest(unittest.TestCase):
#     def test_site_links(self):
#         print 'test_site_links'
#         for query_dic in qs_lst:
#             keywords = query_dic['keywords']  #query text
#             pages_cnt = query_dic['pages_cnt']
#             links_per_page = query_dic['links_per_page']
#             print '-------------------------------------------------------------------------'
#             print 'QUERY:', keywords, '  Pages count:', pages_cnt, '  Links per page:', links_per_page
#
#             squery = create_squery(keywords)
#             links_iter = result_links_iter(squery)
#             last_page_num = 0
#             link_cnt = links_per_page
#             for url, page_num, pos_in_page in links_iter:
#                 print 'page_num:', page_num, 'pos_in_page:', pos_in_page, 'url:', url
#                 if last_page_num != page_num:
#                     self.assertEqual(last_page_num + 1, page_num, 'Order of pages is wrong %d, %d' %
#                                                                   (last_page_num, page_num))
#                     last_page_num += 1
#
#                 if pos_in_page == 0:
#                     self.assertEqual(link_cnt, links_per_page, 'Incorrect links count %d for page %d'
#                                                                % (link_cnt, last_page_num))
#                     link_cnt = 1
#                 else:
#                     link_cnt += 1
#                     self.assertEqual(link_cnt, pos_in_page + 1,
#                                      'Incorrect links order %d, %d ' % (link_cnt, pos_in_page))
#
#                 match_obj = match(url)
#                 self.assertIsNotNone(match_obj, 'Wrong url "%s"' % url)
#
#             self.assertEqual(last_page_num + 1, pages_cnt, 'Wrong pages number %d' % last_page_num)
#
#     def test_find_rank(self):
#         for keywords, site_lst in query_site_rank_tree().iteritems():
#             squery = create_squery(keywords)
#             site_rank_lst = [create_site_rank_dic(website_id=get_website_id(site['url']),
#                                                   site_url=site['url'],
#                                                   squery_id=get_query_id(keywords),
#                                                   keywords=keywords) for site in site_lst]
#
#             for site_rank in find_rank(squery, site_rank_lst):
#                 self.assertTrue(self.check_site_rank(site_rank, site_lst))
#
#     def check_site_rank(self, site_rank, site_lst):
#         for site in site_lst:
#             if site_rank['url'] == site['url']:
#                 if site_rank['page_num'] == site['page_num'] and \
#                                 site_rank['pos_in_page'] == site['pos_in_page']:
#                     return True
#                 else:
#                     return False
#         else:
#             raise ItemNotFoundError('Page url \'%s\' was not found in pages list' % site_rank['url_txt'])
#
# if __name__ == "__main__":
#     unittest.main()
#

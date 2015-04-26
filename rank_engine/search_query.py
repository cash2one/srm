#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['find_rank']

from browser import browse_pages, save_pages
from lxml import html
import logging
from html_storage import create_subfolder

# import os
import re
# import query_samples as qs

URL_PREFIX = '/url?q='


class LocalBreak(Exception):
    """ class is used to exit from many nested loops via exception raising
    """
    pass


def find_rank(search_query, website_lst):
    """ Iterator finds ranks for many pages searched in one google query

    :param search_query: google query
    :param website_lst: list of pages
    :return: page rank via yield operator

    """
    logging.info('-------------------- New Search Query ------------------------')
    logging.info(search_query)

    create_subfolder(search_query['keywords'])

    rpp = search_query['results_per_page']
    # set of sites id of which still are not found in google links
    rem_sites = set([website['website_id'] for website in website_lst])
    logging.info(rem_sites)

    #nothing to search
    if len(rem_sites) == 0:
        return

    try:
        print search_query
        print website_lst
        for google_link, page_n, pos_n in result_links_iter(search_query):
            site_pos = page_n * rpp + pos_n
            print page_n, pos_n
            logging.debug('page:' + str(page_n) + ' pos in page:' + str(pos_n) + ' site pos:' + str(site_pos))
            for website in website_lst:
                #print website
                website_id = website['website_id']
                if website_id in rem_sites:
                    if compare_url(google_link, website['url']):
                        website['site_pos'] = site_pos
                        rem_sites.remove(website_id)

                        logging.info('Rank found for site %s: rank - %d, link -  %s' % (website['url'],
                                                                            website['site_pos'],
                                                                            google_link))
                        print website['url']
                        yield {'group_id': search_query['group_id'],
                               'website_id': website['website_id'],
                               'keywords_id': search_query['keywords_id'],
                               'site_pos': page_n * rpp + pos_n  # position index starts from 0
                        }
                        #exit from all loops
                        if len(rem_sites) == 0: #all sites were found
                            raise LocalBreak()
        else:  # view all pages, some sites were not found
            print 'not found', rem_sites
            assert len(rem_sites) != 0
            for website_id in rem_sites:
                yield {'group_id': search_query['group_id'],
                       'website_id': website_id,
                       'keywords_id': search_query['keywords_id'],
                       'site_pos': -int(search_query['results_cnt'])
                }

    except LocalBreak:
        pass


def extract_href_lst(tree):
    url_lst = [item.attrib['href'] for item in tree.xpath('//h3[@class="r"]/a')]
    return url_lst


def result_links_iter(squery):
    #page and position index start from 0
    pages = browse_pages(squery)
    for page_n, page in enumerate(pages):
        tree = html.fromstring(page)
        href_lst = extract_href_lst(tree)
        url_lst = [extract_url(href) for href in href_lst if href[0:len(URL_PREFIX)] == URL_PREFIX]
        for pos_in_page, url in enumerate(url_lst):
            yield url, page_n, pos_in_page


def ctext(el):
    result = []
    if el.text:
        result.append(el.text)
    for sel in el:
        #        print sel.tag
        if sel.tag == "b":
            result.append(ctext(sel))
        if sel.tail:
            result.append(sel.tail)
    return "".join(result)


def create_squery(keywords,
                   tld='com',
                   lang='en',
                   results_per_page=10,
                   results_cnt=50,
                   min_pause=10,
                   max_pause=30):
    return {'keywords': keywords,
            'tld': tld,
            'lang': lang,
            'results_per_page': results_per_page,
            'results_cnt': results_cnt,
            'min_pause': min_pause,
            'max_pause': max_pause}


def create_site_rank_dic(website_id, url, squery_id, keywords):
    site_rank = {'website_id': website_id,
                 'url': url,
                 'squery_id': squery_id,
                 'keywords': keywords,
                 'site_pos': 0
    }
    return site_rank


def extract_url(url_str):
    """
    string sample:
    /url?q=http://www.wikihow.com/Refinish-Antique-Furniture&sa=U&ei=0sxkU_KbOObl4QSD8oC4Ag&ved=0CCwQFjAA&usg=AFQjCNGe99KRKPYNSOTqRxW_K70ydd_vzw
    """
    obj = re.search('&', url_str)
    start_pos = len(URL_PREFIX)
    end_pos = obj.start()
    url = url_str[start_pos: end_pos]
    return url


def compare_url(google_link_url_str, site_url_str, exact_compare=False):
    if exact_compare:
        return google_link_url_str == site_url_str
    else:
        #site name might be included in the google_link
        return site_url_str in google_link_url_str


if __name__ == '__main__':
    pass



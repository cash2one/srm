#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['browse_pages', 'save_pages', 'prepare_google_query', 'is_load_from_file']

import os
import sys
import socket
import errno
import urllib2
import httplib
import logging
from time import sleep
from random import randint
from rank_params import PARAMS
from html_storage import add_page, add_search_query


_MAX_ATTEMP_ = 5

# if sys.version_info[0] > 2:
#     from http.cookiejar import LWPCookieJar
#     from urllib.request import Request, urlopen
#     from urllib.parse import quote_plus, urlparse, parse_qs
# else:
from cookielib import LWPCookieJar
from urllib import quote_plus
from urllib2 import Request, urlopen
from urlparse import urlparse, parse_qs


# URL templates to make Google searches.
url_home_template = "http://www.google.%(tld)s/"
url_search_template = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(keywords)s&btnG=Google+Search&inurl=https"
url_next_page_template = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(keywords)s&start=%(start)d&inurl=https"
url_search_num_template = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(keywords)s&num=%(results_per_page)d&btnG=Google+Search&inurl=https"
url_next_page_num_template = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(keywords)s&num=%(results_per_page)d&start=%(start)d&inurl=https"

# PAGES_FOLDER = r'D:\PycharmProjects\page_rank\rank_query\pages'


class FileNotFoundException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Cookie jar. Stored at the user's home folder.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'  # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass


def save_pages(squery, file_name, folder_path=PARAMS['HTML_PAGES_FOLDER'], results=20):
    g_pages = browse_pages_from_internet(squery, stop=results)

    for page_n, page in enumerate(g_pages):
        full_file_name = os.path.join(folder_path, file_name + '_' + str(page_n + 1) + '.html')
        print full_file_name
        with open(full_file_name, 'w') as f:
            f.write(page)


def get_page(url):
    """
    Request the given URL and return the response page, using the cookie jar.

    @type  url: str
    @param url: URL to retrieve.

    @rtype:  str
    @return: Web page retrieved for the given URL.

    @raise IOError: An exception is raised on error.
    @raise urllib2.URLError: An exception is raised on error.
    @raise urllib2.HTTPError: An exception is raised on error.
    """

    request = Request(url)
    request.add_header('User-Agent',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    cookie_jar.add_cookie_header(request)
    response = urlopen(request)
    cookie_jar.extract_cookies(response, request)
    html = response.read()
    response.close()
    cookie_jar.save()
    return html


def browse_pages(squery):
    if is_load_from_file():
        file_name = squery['keywords'].replace(' ', '_')
        pages = browse_pages_from_file(html_pages_folder(), file_name)
    else:
        pages = browse_pages_from_internet(squery['keywords'],
                                             tld=squery['tld'],
                                             lang=squery['lang'],
                                             results_per_page=int(squery['results_per_page']),
                                             start=0,
                                             stop=int(squery['results_cnt']))
    return pages


# Returns a generator that yields URLs.
def browse_pages_from_internet(keywords,
                               tld='com',
                               lang='en',
                               results_per_page=10,
                               start=0,
                               stop=0,
                               min_pause=10,
                               max_pause=30):
    """
    Search the given keywords string using Google.

    @type  keywords: str
    @paquery_txtuery: Query string. Must NOT be url-encoded.

    @type  tld: str
    @param tld: Top level domain.

    @type  lang: str
    @param lang: Languaje.

    @type  results_per_page: int
    @param results_per_page: Number of results per page.

    @type  start: int
    @param start: First result to retrieve.

    @type  stop: int
    @param stop: Last result to retrieve.
        Use C{0} to keep searching forever.

    @type  pause: float
    @param pause: Lapse to wait between HTTP requests.
        A lapse too long will make the search slow, but a lapse too short may
        cause Google to block your IP. Your mileage may vary!

    @type  only_standard: bool
    @param only_standard: If C{True}, only returns the standard results from
        each page. If C{False}, it returns every possible link from each page,
        except for those that point back to Google itself. Defaults to C{False}
        for backwards compatibility with older versions of this module.

    @rtype:  generator
    @return: Generator (iterator) that yields found URLs. If the C{stop}
        parameter is C{None} the iterator will loop forever.
    """

    # Set of hashes for the results found.
    # This is used to avoid repeated results.
    #hashes = set()

    # Prepare the search string.
    subfolder = keywords.strip()
    keywords = quote_plus(keywords)

    # Grab the cookie from the home page.
    url_home = url_home_template % vars()
    add_search_query(subfolder, 0, url_home)

    # get_page2(url_home, min_pause, max_pause)
    get_page(url_home)

    # Prepare the URL of the first request.
    # if start:
    #     if results_per_page == 10:
    #         url = url_next_page_template % vars()
    #     else:
    #         url = url_next_page_num_template % vars()
    # else:
    #     if results_per_page == 10:
    #         url = url_search_template % vars()
    #     else:
    #         url = url_search_num_template % vars()

    url = prepare_google_query(keywords, tld, lang, results_per_page=results_per_page, start=start)
    add_search_query(subfolder, 1, url)

    # Loop until we reach the maximum result, if any (otherwise, loop forever).
    while stop == 0 or start < stop:

        # Sleep between requests.
        # time.sleep(pause)
        sleep_random(min_pause, max_pause)

        # Request the Google Search results page.
        html = get_page2(url, min_pause, max_pause)
        add_page(subfolder, int(start)/results_per_page + 1, html)
        # Yield the result.
        yield html

        # Prepare the URL for the next request.
        start += results_per_page
        # if results_per_page == 10:
        #     url = url_next_page_template % vars()
        # else:
        #     url = url_next_page_num_template % vars()
        url = prepare_google_query(keywords, tld, lang, results_per_page=results_per_page, start=start)
        if start < stop:
            add_search_query(subfolder, int(start)/results_per_page + 1, url)


def get_page2(url, min_pause, max_pause):
    for y in xrange(_MAX_ATTEMP_):
        try:
            html = get_page(url)
            break
        # except socket.error as error:
        #     html = None
        except urllib2.URLError as e:
            print "Url open error: "
            if hasattr(e, 'reason'):
                logging.critical('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                logging.critical('Error code: ', e.code)
            logging.error("Attempting %d of %d" % (y + 1, _MAX_ATTEMP_))
            sleep_random(min_pause, max_pause)
        except httplib.BadStatusLine as e:
            logging.critical("httplib.BadStatusLine error")
            logging.critical(e)
            logging.error("Attempting %d of %d" % (y + 1, _MAX_ATTEMP_))
            sleep_random(min_pause, max_pause)
        except socket.error as e:
            logging.critical("socket.error")
            logging.critical(e)
            logging.error("Attempting %d of %d" % (y + 1, _MAX_ATTEMP_))
            sleep_random(min_pause, max_pause)
        except:
            logging.critical("Unknown error")
            logging.critical("Attempting %d of %d" % (y + 1, _MAX_ATTEMP_))
            sleep_random(min_pause, max_pause)
    else:
        logging.critical("Can not receive the response")
        html = None
    return html


def prepare_google_query(keywords, tld='com', lang='en', results_per_page=10, start=0):
    # Prepare the search string.
    keywords = quote_plus(keywords)

    # Grab the cookie from the home page.

    # Prepare the URL of the first request.
    if start:
        if results_per_page == 10:
            url = url_next_page_template % vars()
        else:
            url = url_next_page_num_template % vars()
    else:
        if results_per_page == 10:
            url = url_search_template % vars()
        else:
            url = url_search_num_template % vars()
    return url


def browse_pages_from_file(folder_path, file_name):
    full_file_name = os.path.join(folder_path, file_name + '_1.html')
    if not os.path.isfile(full_file_name):
        raise FileNotFoundException('File %s was not found' % (full_file_name,))
    i = 1
    while True:
        full_file_name = os.path.join(folder_path, file_name + '_' + str(i) + '.html')
        # print full_file_name
        if not os.path.isfile(full_file_name):
            break
        with open(full_file_name, 'r') as f:
            page = f.read()
        yield page
        i += 1


def is_load_from_file():
    return PARAMS['LOAD_FROM_FILE']


def html_pages_folder():
    return PARAMS['HTML_PAGES_FOLDER']


def sleep_random(min_pause, max_pause):
    #calc time of sleeping
    pause = randint(min_pause, max_pause)
    # print 'Slipping ', pause
    sleep(pause)


if __name__ == "__main__":
    pass


#!/usr/bin/python
# -*- coding: utf-8 -


__all__ = ['squery_samples_lst', 'query_site_rank_tree', 'site_query_rank_tree', 'get_website_id',
           'get_query_id', 'ItemNotFoundError']

from rank_engine.rank_monitor import connect_to_db


class IncorrectTableStateException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ItemNotFoundError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


search_group_samples = {
    'Aroundafricasafari': {
        'site_lst': ({'url': 'http://aroundafricasafari.com', 'title': 'Aroundafricasafari.com'},),
        'keywords_lst': ({'keywords': 'African Safaris', },
                         {'keywords': 'African Safari Tours', },
                         {'keywords': 'Africa Safaris', },
                         {'keywords': 'Safaris in Africa', },
                         {'keywords': 'Safaris in Uganda', },
                         {'keywords': 'Safari Tours Uganda', },
                         {'keywords': 'Uganda Safaris', },
                         {'keywords': 'Uganda Safari Tours', },
        )
    },

    'Ashlarlandscapes': {
        'site_lst': ({'url': 'http://ashlarlandscapes.com', 'title': 'Ashlarlandscapes.com'},),
        'keywords_lst': ({'keywords': 'ancaster landscaping', },
                         {'keywords': 'backyard design', },
                         {'keywords': 'burlington landscaping', },
                         {'keywords': 'burlington landscaping company', },
                         {'keywords': 'landscape design', },
                         {'keywords': 'landscaping', },
                         {'keywords': 'landscaping companies', },
                         {'keywords': 'mississauga landscaping', },
                         {'keywords': 'oakville landscaping', },
                         {'keywords': 'oakville landscaping company', },
                         {'keywords': 'snow and ice removal', },
                         {'keywords': 'snow removal burlington', },
                         {'keywords': 'snow removal service oakville', },
        )
    },

    'Autoglassrepairs': {
        'tld': 'ca',
        'site_lst': ({'url': 'http://autoglassrepairs.ca', 'title': 'Autoglassrepairs.ca'},),
        'keywords_lst': ({'keywords': 'Auto Glass Repair Toronto', },
                         {'keywords': 'AutoGlass Repair Toronto', },
                         {'keywords': 'Auto Glass Toronto', },
                         {'keywords': 'AutoGlass Toronto', },
                         {'keywords': 'Toronto AutoGlass', },
                         {'keywords': 'Toronto Auto Glass', },
                         {'keywords': 'Toronto Auto Glass Repair', },
                         {'keywords': 'Toronto AutoGlass Repair', },
        )
    },

    'Bodybijou': {
        'site_lst': ({'url': 'http://bodybijou.com', 'title': 'Bodybijou.com'},),
        'keywords_lst': ({'keywords': 'belly chain', },
                         {'keywords': 'belly chains', },
                         {'keywords': 'body chain', },
                         {'keywords': 'body chain jewelry', },
                         {'keywords': 'body chain necklace', },
                         {'keywords': 'body chains', },
                         {'keywords': 'body jewelry', },
                         {'keywords': 'body necklace', },
                         {'keywords': 'bracelet with ring', },
                         {'keywords': 'bracelet with ring attached', },
                         {'keywords': 'finger bracelet', },
                         {'keywords': 'handmade jewelry', },
                         {'keywords': 'jewelry online', },
                         {'keywords': 'leg chain', },
                         {'keywords': 'ringalet', },
                         {'keywords': 'ring bracelet', },
                         {'keywords': 'shoulder necklace', },
                         {'keywords': 'unique jewelry', },
                         {'keywords': 'waist chain', },
                         {'keywords': 'waist chains', },
        )
    },

    'Bountifulfruitarrangements': {
        'site_lst': ({'url': 'http://bountifulfruitarrangements.com', 'title': 'Bountifulfruitarrangements.com'},),
        'keywords_lst': ({'keywords': 'edible arrangements', },
                         {'keywords': 'edible fruit arrangements', },
                         {'keywords': 'fresh fruit basket', },
                         {'keywords': 'Fruit Baskets Toronto', },
                         {'keywords': 'fruit bouquets', },
                         {'keywords': 'Toronto Edible Fruit Arrangements', },
        )
    },

    'Brinkleydentalgroup': {
        'site_lst': ({'url': 'http://brinkleydentalgroup.com', 'title': 'Brinkleydentalgroup.com'},),
        'keywords_lst': ({'keywords': 'best dentist in brampton', },
                         {'keywords': 'brampton dentist', },
                         {'keywords': 'dentist brampton', },
                         {'keywords': 'dentist in brampton', },
                         {'keywords': 'dentists in brampton', },
        )
    },

    'Ccproducts': {
        'tld': 'ca',
        'site_lst': ({'url': 'http://Ccproducts.ca', 'title': 'Ccproducts.ca', },),
        'keywords_lst': ({'keywords': 'concrete expansion joint filler', },
                         {'keywords': 'concrete sealer', },
                         {'keywords': 'de-icing solution', },
                         {'keywords': 'de-icing solutions', },
                         {'keywords': 'expansion joint filler', },
                         {'keywords': 'liquid de-icer', },
                         {'keywords': 'liquid de-icers', },
                         {'keywords': 'natural stone', },
                         {'keywords': 'natural stone ledgestone', },
                         {'keywords': 'natural stone sealer', },
                         {'keywords': 'natural stone toronto', },
                         {'keywords': 'natural thin stone veneers', },
                         {'keywords': 'paving stone sealer', },
                         {'keywords': 'stone veneer panels', },
                         {'keywords': 'stone veneers toronto', },
                         {'keywords': 'winter products', },
        )
    },
}


def clear_db():
    db = connect_to_db()
    cur = db.cursor()
    cur.execute("""DELETE FROM srm_website_rank; """)
    cur.execute("""DELETE FROM srm_website; """)
    cur.execute("""DELETE FROM srm_keywords; """)
    cur.execute("""DELETE FROM srm_search_group; """)
    db.commit()
    db.close()


def populate_db():
    db = connect_to_db()
    cur = db.cursor()
    for group_name, s_group in search_group_samples.items():
        group_id = write_search_group_tbl(cur,
                                          group_name,
                                          s_group.get('tld', 'com'),
                                          s_group.get('lang','en'),
                                          s_group.get('results_cnt', 100))
        print group_id

        for site in s_group['site_lst']:
            website_id = write_website_tbl(cur, group_id, site['url'], site['title'])
            print website_id

        for keywords_dic in s_group['keywords_lst']:
            keywords_id = write_keywords_tbl(cur, group_id, keywords_dic['keywords'])
            print 'keywords_id', keywords_id
    db.commit()
    db.close()


def write_search_group_tbl(cur, group_name, tld, lang, results_cnt ):
    cur.execute("""SELECT id FROM srm_search_group WHERE group_name=%s;""", (group_name,))
    rs = cur.fetchall()
    if len(rs) > 1:
        raise IncorrectTableStateException('Table srm_search_group has duplicate group %s' % group_name)
    elif len(rs) == 1:
        group_id = rs[0][0]
    elif len(rs) == 0:
        cur.execute("""INSERT INTO srm_search_group(group_name,
                           top_level_domain,
                           lang,
                           results_per_page,
                           results_cnt) VALUES(%s, %s, %s, %s, %s);""",
                    (group_name, tld, lang, 10, results_cnt))
        cur.execute("""SELECT id FROM srm_search_group WHERE group_name=%s;""", (group_name,))
        rs = cur.fetchall()
        group_id = rs[0][0]

    return group_id


def write_website_tbl(cur, group_id, site_url, site_title):
    cur.execute("""SELECT id FROM srm_website WHERE search_group_id=%s AND url=%s;""", (group_id, site_url,))
    rs = cur.fetchall()
    if len(rs) > 1:
        raise IncorrectTableStateException('Table website has duplicate site %s' % site_url)
    elif len(rs) == 1:
        website_id = rs[0][0]
    elif len(rs) == 0:
        cur.execute("""INSERT INTO srm_website(search_group_id, url, title) VALUES (%s, %s, %s);""",
                    (group_id, site_url, site_title))
        cur.execute("""SELECT id FROM srm_website WHERE search_group_id=%s AND url=%s;""", (group_id, site_url,))
        rs = cur.fetchall()
        website_id = rs[0][0]

    return website_id


def write_keywords_tbl(cur, group_id, keywords):
    cur.execute("""SELECT id FROM srm_keywords WHERE search_group_id=%s AND keywords=%s;""",
                (group_id, keywords,))
    rs = cur.fetchall()
    if len(rs) > 1:
        raise IncorrectTableStateException('Table squery has duplicate keywords %s' % keywords)
    elif len(rs) == 1:
        keywords_id = rs[0][0]
    elif len(rs) == 0:
        cur.execute("""INSERT INTO srm_keywords(keywords, search_group_id) VALUES(%s, %s);""",
                    (keywords, group_id))
        cur.execute("""SELECT id FROM srm_keywords WHERE search_group_id=%s AND keywords=%s;""",
                (group_id, keywords,))
        rs = cur.fetchall()
        keywords_id = rs[0][0]

    return keywords_id


if __name__ == '__main__':
    clear_db()
    populate_db()

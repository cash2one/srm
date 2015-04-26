# -*- coding: utf-8 -*-

# Create your views here.

# from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template.context import RequestContext
from django.db import connection
# import time
# import datetime
from datetime import date, timedelta
from apps.dashboard.models import find_nearest_date
from srm_model.raw_sql import rank_changes_sql
from forms import PositionsByDate
from srm_model.models import SearchGroup
from django.db.models.loading import get_model
from srm_model.models import SearchGroup, Keywords, Website

def homepage(request, template_name="dashboard.html"):
    # wr = get_model(u'srm_model', 'WebsiteRank', seed_cache=False, only_installed=False)
    # o = wr(website_pos=111, rank_date='2014-03-03')
    # sg = SearchGroup.objects.get(pk=33)
    # o.search_group = sg
    # ws = Website.objects.get(pk=32)
    # o.website = ws
    # kw = Keywords.objects.get(pk=188)
    # o.keywords = kw
    # o.save()
    if request.method == 'POST':
        form = PositionsByDate(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            date1 = cd['date1']
            date2 = cd['date2']
            named_rows = rank_changes_sql(date1, date2)
        else:
            # TODO: add error message
            date1 = None
            date2 = None
            named_rows = None
    else:
        date1 = find_nearest_date(date.today())
        if date1 is None:
            #empty report
            date1 = None
            date2 = None
            named_rows = None
        else:
            date2 = (date1 - timedelta(days=1))
            named_rows = rank_changes_sql(date1, date2)
            form = PositionsByDate(initial={'date1': date1, 'date2': date2})

    return render(request, template_name,
                  {'menu': 'dashboard',
                   'rows_lst': named_rows,
                   'date1': date1.strftime("%m/%d/%Y"),
                   'date2': date2.strftime("%m/%d/%Y"),
                   'form': form}
    )


def dict_fetchall(cursor):
    """Returns all rows from a cursor as a dict
    """
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


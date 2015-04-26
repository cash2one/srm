# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db import connection


def homepage(request, template_name="settings.html"):
        # cursor = connection.cursor()
        # cursor.execute(DAY_RANK__RPT_SQL, [date1, date2])
        # pos_lst = dict_fetchall(cursor)
        return render_to_response(template_name,
            {'menu': 'settings'},
            context_instance=RequestContext(request, {}))

# -*- coding: utf-8 -*-

from django import forms
import datetime
from django.forms.extras.widgets import SelectDateWidget


class PositionsByDate(forms.Form):
    date1 = forms.DateField(widget=SelectDateWidget())
    date2 = forms.DateField(widget=SelectDateWidget())

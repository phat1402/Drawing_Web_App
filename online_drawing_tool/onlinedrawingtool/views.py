import random
import re

import requests
from django.core.cache import cache
from django.db.models import Count, Max, Avg, F, IntegerField, Sum, Case, When
from django.views import generic
from django.views.generic.base import ContextMixin
from api.models import UserInfor

class HomePage(generic.TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return super(HomePage,self).get(request, *args, **kwargs)

# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Copyright (C) 2022 OSG.
#
"""

Command to find urls op vacatures sites


"""

__author__ = 'sergej[A]dergatsjev[D]be (Sergej Dergatsjev)'

from django.db import models, IntegrityError, DatabaseError
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.http import urlunquote as dj_urlunquote
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from haystack.query import SearchQuerySet, AutoQuery
from django.template.defaultfilters import slugify
from django.utils import translation
from permanentjob.models import *
import random
from django import db
import os


#settings.SITEMAP_PATH
SITEMAP_BASE_PATH = "/home/sites/vacaturestoday/data"

ADS_PER_PAGE_EMPTY = 10
ADS_PER_PAGE = 7
RESULTS_PER_PAGE = 50
CAT_FOLDER = "/cat/"



class Command(BaseCommand):
    #def add_arguments(self, parser):
        #parser.add_argument('--model', dest='model', default="all", help='Specify model: category, location, company, statickeyword, city, all')

    def handle(self, *args, **options):
        """
        command for count
        """
        translation.activate(settings.LANGUAGE_CODE)
        cats = self.get_cats()
        for cat in cats:
            self.gen_cat(cat)

    def get_cats(self):
        cats = PermanentJob.objects.values_list('industry', flat=True).distinct()
        return cats

    def gen_cat(self, cat):
        permanentjobs = PermanentJob.objects.filter(industry=cat)
        paginator = Paginator(permanentjobs, RESULTS_PER_PAGE)
        print('Jobs count: ' +  str(permanentjobs.count())) 
        data = self.get_data()
        data['industry'] = cat 
        data['page_range'] = paginator.page_range
        # Get category mapper for description and labels for SEO
        # Met labels kunnen we Eigenlijk nog extra navigatie maken
        # Zodat labels beter verdelen vacatures 
        # Labels en Categorien kunnen in hun buurt ook objecten 
        # zijn met volledige tekst van onder zodat ze komen naar boven 
        for page_num in paginator.page_range:
            page = paginator.page(page_num)
            data['current_page'] = page_num
            data['jobs'] = page.object_list
            data['title'] = self.create_title(cat, page.object_list)
            data['description'] = self.create_description(page.object_list)
            name = '%s%s.html' % (cat, str(page_num))
            self.save_file(CAT_FOLDER, data, name)
        db.connections.close_all()
       
    def create_title(self, cat, jobs):
        title = ""
        for job in jobs[:3]:
            title = title + " " + job.title
        title = cat + ": " + title
        return title
        

    def create_description(self,  jobs):
        title = ""
        for job in jobs[3:]:
            if title == "":
                title = job.title
            else:
                title = title + " " + job.title
        return title
 
    def get_data(self):
        data = {
            "jobsite_name": settings.JOBSITE_NAME,
            "jobsite_domain": settings.JOBSITE_DOMAIN,
            "country": settings.COUNTRY,
            "iso_lang": settings.ISO_LANG,
            "my_datepicker_format": settings.MY_DATEPICKER_FORMAT,
            "permanentjob_map": settings.PERMANENTJOB_MAP,
        }
        return data

    def save_file(self, folder, data, name):
        #result_html = render_to_string('job/static_page.html', data)
        data["canonical"] = "https://" + data["jobsite_domain"] + folder + name
        result_html = render_to_string('permanentjob/cat.amp.html', data)
        path = SITEMAP_BASE_PATH + folder + name
        self.get_path(path)
        f = open(path, "w")
        #import pdb;pdb.set_trace()
        f.write(result_html) #.encode("utf-8"))
        f.close()

    def rm_file(self, folder, name):
        path = keyword_base_path + folder + name
        if os.path.exists(path):
            os.remove(path)


    def get_path(self, checked_path):
        if not os.path.exists(os.path.dirname(checked_path)):
            try:
                os.makedirs(os.path.dirname(checked_path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise


    def get_payed_results(self, job):
        ads = None
        base_sqs = SearchQuerySet().using('default').filter_and(payed=True)
        for term in job.keywords.select_related():    
            term_sqs = base_sqs.filter_and(content=AutoQuery(term.name))
            if term_sqs.count() >= ADS_PER_PAGE:
                ads = term_sqs
                break
        if not ads or ads.count() == 0:
            last_days = date.today() - timedelta(days=7)
            ads = random.sample(list(base_sqs.filter(online_since_refreshed__gte=last_days)), k=ADS_PER_PAGE_EMPTY)
        else:
            ads = ads.order_by('weight', '-most_recent', '-_score')[:ADS_PER_PAGE]
        return ads


# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Copyright (C) 2019 Web App Development EEOD 
#
# 
__author__ = 'sergej[A]dergatsjev[D]be (Sergej Dergatsjev)'

from django.db import models, IntegrityError, DatabaseError
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.http import urlunquote as dj_urlunquote
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.utils import translation
from permanentjob.models import *
import random
from django import db
import os
from datetime import datetime
from datetime import date, timedelta
import textile
import docx2txt
import glob

#DOCS_PATCH = "/home/sites/vacaturestoday/data/text/Teksten/Wiraisha/Niet gepubliceerd betaald/IT/"
#INDUSTRY = "Informatics"

#DOCS_PATCH = "/home/sites/vacaturestoday/data/text/Teksten/Wiraisha/Niet gepubliceerd betaald/Accounting boekhouders/"
#DOCS_PATCH = "/home/sites/vacaturestoday/data/text/Teksten/Wiraisha/Niet gepubliceerd betaald/accounting_boekhouders_2/"
#DOCS_PATCH = "/home/sites/vacaturestoday/data/text/Teksten/Wiraisha/Niet gepubliceerd betaald/Accounting_boekhouders_3/"
#INDUSTRY = "Accounting"

#DOCS_PATCH = "/home/sites/vacaturestoday/data/text/Teksten/Wiraisha/Niet gepubliceerd betaald/StepStone_Engineering_305/"
#DOCS_PATCH = "/home/sites/vacaturestoday/data/text/Teksten/Wiraisha/Niet gepubliceerd betaald/Stepstone_engineering_vacature_277/"
#DOCS_PATCH = "/home/sites/vacaturestoday/data/text/Teksten/Wiraisha/Niet gepubliceerd betaald/Stepstone_engineering_vacatures_2_95/"
#DOCS_PATCH = "/home/sites/vacaturestoday/data/text/Teksten/Wiraisha/Niet gepubliceerd betaald/Technishe_2/"
#DOCS_PATCH = "/home/sites/vacaturestoday/data/text/Teksten/Wiraisha/Niet gepubliceerd betaald/Technishe_beroepen_betaald/"
#INDUSTRY = "Technical"

#DOCS_PATCH = "/home/sites/vacaturestoday/data/text/Teksten/Wiraisha/Niet gepubliceerd betaald/Transport_Logistiek/"
DOCS_PATCH = "/home/sites/vacaturestoday/data/text/Teksten/Wiraisha/Niet gepubliceerd betaald/Transport_Logistiek2/"
INDUSTRY = "Logistics"

class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        # Read files
        docs = glob.glob(DOCS_PATCH + "*.docx")
        # Convert files
        #import pdb;pdb.set_trace()
        for doc in docs:
            title = self.get_title(doc)
            text = docx2txt.process(doc)
            html = textile.textile(text)
            self.create_jobpost(title, text, html)
        # Save files in database   

    def get_title(self, doc):
        title = os.path.basename(doc)
        title = title.replace(".docx", "")
        return title

    def create_jobpost(self, title, text, html):
        obj = PermanentJob()
        obj.url = slugify(title)
        obj.title = title
        obj.date_posted = datetime.now() 
        obj.valid_through = (date.today()+timedelta(days=60)).isoformat() 
        obj.description = text
        obj.raw_text = html
        obj.industry = INDUSTRY
        obj.company_name = "Global Recruitment"
        try:
            obj.save()
        except:
            print(obj.url)
            #/home/sites/vacaturestoday/data            
        # obj.address = "" Ik moet iets ontdenken met adresse # random bussiness centers and co working spaces in belgium.
        # Een aparte command schrijven ervoor
        #obj.media_img = "" # Logo via Firebase ( Als url local of extern )  
         

         

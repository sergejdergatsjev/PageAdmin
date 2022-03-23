# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Copyright (C) 2022 Web App Development EEOD 
#
# 
__author__ = 'sergej[A]dergatsjev[D]be (Sergej Dergatsjev)'

from django.db import models, IntegrityError, DatabaseError
from django.core.management.base import BaseCommand
from django.conf import settings
from permanentjob.models import *
from django import db
from datetime import datetime
import sys, traceback
from bs4 import BeautifulSoup
    
class Command(BaseCommand):
    def handle(self, *args, **options):
        jobs = PermanentJob.objects.all() #filter(raw_text__icontains="<script")
        #import pdb;pdb.set_trace() 
        for job in jobs:
            soup = BeautifulSoup(job.raw_text, "html.parser")
            soup = self.clean_script(soup)
            job.raw_text = str(soup)
            job.description = self.clean_tags(soup)
            job.save()

    def clean_tags(self, soup):
        return ' '.join(soup.stripped_strings)

    def clean_script(self, soup):
        for data in soup(['iframe', 'script']):
        # Remove tags
            data.decompose()
        return soup

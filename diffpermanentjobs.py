# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Copyright (C) 2019 Web App Development EEOD 
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

class Command(BaseCommand):
    def handle(self, *args, **options):
        jobs = PermanentJob.objects.all()
        self.used = {}
        self.same = {}
        self.report_name = datetime.now()
        DubbeleContent.objects.all().delete()
        for job in jobs:
            self.find_same(job, jobs)
        print("Count:" + str(len(self.same)))
        #self.create_txt_report() # afdrukken om per email door te sturen of via chat dellen
        self.save_reports_in_model()

    def save_reports_in_model(self):
        for k,v in self.same.items():
            self.save_same_in_model(k, v)

    def save_same_in_model(self, key, value):
        job = PermanentJob.objects.get(id=key)
        for same_text in value:
            some_job = PermanentJob.objects.get(id=same_text[0])
            dc = DubbeleContent()
            dc.job = job
            dc.same_with = some_job
            dc.same_text = same_text[1]
            dc.name = self.report_name
            try:
                dc.save()
            except:
                traceback.print_exc(file=sys.stdout)
             
    def create_txt_report(self):
        for k,v in self.same.items():
            print("---------------------- " + str(k) + " ----------------")
            print("pagina's: " + str(len(v)))
            for same_text in v:
                print(same_text[0])
                print(same_text[1])
            print("--------------------- //// -------------------------")

    def is_not_used(self, job_id):
        if (job_id in self.used):
            return False
        else:
            self.used[job_id] = ""
            return True


    def find_same(self, job, jobs):
        for current_job in jobs:
            if current_job != job:
                same = set(job.description.split('\n')).intersection(current_job.description.split('\n'))
                if(len(str(same)) > 200) and (self.is_not_used(current_job.id)):
                    self.add_same(job, current_job, same)
        
    def add_same(self, job, current_job, same):
        job_key = self.same.get(job.id)
        if job_key:
            self.same[job.id].append((current_job.id, same))
        else:
            self.same[job.id] = [(current_job.id, same)]

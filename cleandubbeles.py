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
        dubbels = DubbeleContent.objects.all()
        for dubble in dubbels:
            self.remove_exact(dubble)

    def remove_exact(self, dubble):
        exact = DubbeleContent.objects.filter(job=dubble.same_with, same_with=dubble.job)
        print(exact.count())
        if(exact.count() == 1):
            exact.delete()
        elif(exact.count() > 1):
            import pdb;pdb.set_trace()
        else:
            pass

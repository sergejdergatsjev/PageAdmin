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
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.utils import translation
from permanentjob.models import *
import random
from django import db
import os
from datetime import datetime
from datetime import date, timedelta
from oauth2client import client
from googleapiclient import sample_tools

INDUSTRY = "Administratief"

class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        service, flags = sample_tools.init(args, 'blogger', 'v3', __doc__, __file__,
            scope='https://www.googleapis.com/auth/blogger') 
        try:
            
            users = service.users()
            # Retrieve this user's profile information
            thisuser = users.get(userId='self').execute()
            print('This user\'s display name is: %s' % thisuser['displayName'])
            blogs = service.blogs()
            # Retrieve the list of Blogs this user has write privileges on
            thisusersblogs = blogs.listByUser(userId='self').execute()
            for blog in thisusersblogs['items']:
                print('The blog named \'%s\' is at: %s' % (blog['name'], blog['url']))
            posts = service.posts()
            import pdb;pdb.set_trace()
            # List the posts for each blog this user has
            for blog in thisusersblogs['items']:
                print('The posts for %s:' % blog['name'])
                request = posts.list(blogId=blog['id']) # ['LIVE', 'DRAFT', 'SCHEDULED'] 
                while request != None:
                    posts_doc = request.execute()
                    if 'items' in posts_doc and not (posts_doc['items'] is None):
                        for post in posts_doc['items']:
                            #import pdb;pdb.set_trace()
                            #print('  %s (%s)' % (post['title'], post['url']))
                            self.create_jobpost(post['title'], post['content'], post['url'], post['selfLink'], post['blog'], post['id'])
                    request = posts.list_next(request, posts_doc)

        except client.AccessTokenRefreshError:
            print ('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize')

    def create_jobpost(self, title, html, url, selflink, blogger_blog_id, blogger_post_id):
        obj = PermanentJob()
        if (url):
            obj.url = url
        obj.blogger_selfLink = selflink
        obj.title = title
        obj.date_posted = datetime.now()
        obj.valid_through = (date.today()+timedelta(days=60)).isoformat() 
        #obj.description = text
        obj.raw_text = html
        obj.industry = INDUSTRY
        obj.company_name = "Global Recruitment"
        obj.blogger_blog_id = blogger_blog_id['id']
        obj.blogger_post_id = blogger_post_id
        try:
            obj.save()
        except:
            #import pdb;pdb.set_trace()
            print("Error")
            print(obj.blogger_blog_id)

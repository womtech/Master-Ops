# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from datetime import datetime
from django.utils import timezone
# Create your models here.

class cms(models.Model):
  cms_id   = models.CharField(max_length= 100, blank=False)
  cms_name = models.CharField(max_length= 100, blank=False)
  is_active = models.BooleanField(default=False, blank=False)

  def __str__(self):
    return self.cms_name

  class Meta:
    verbose_name = "Youtube CMS"
    verbose_name_plural = "Youtube CMS(s)"


class channel(models.Model):
  channel_id   = models.CharField(max_length= 100, blank=False)
  channel_name = models.CharField(max_length= 100, blank=False)
  cms_id 		 = models.ForeignKey(cms, primary_key=False, on_delete=models.CASCADE)
  is_Affiliate_Channel = models.BooleanField(default=False, blank=False)
  is_active 	 = models.BooleanField(default=False, blank=False)
  remarks 		 = models.TextField(default=True, blank=True)

  def __str__(self):
    return self.channel_name

  class Meta:
    verbose_name        = "Youtube Channel"
    verbose_name_plural = "Youtube Channels"


class facebook(models.Model):
  page_id   = models.CharField(max_length= 100, blank=False) 
  page_name = models.CharField(max_length= 100, blank=False)
  url 	  = models.CharField(max_length= 100, blank=False)  
  catagory  = models.CharField(max_length= 100, blank=False)
  sub_catagory  = models.CharField(max_length= 100, blank=False)
  fans = models.PositiveIntegerField( blank=False, default=0)
  ptat = models.PositiveIntegerField( blank=False, default=0)
  token = models.TextField(blank=True)
  tags 	  = models.TextField(default=True, blank = True)
  description = models.TextField(default=True, blank = True)
  remarks = models.TextField(default = False, blank = True)
  is_active = models.BooleanField(default=False, blank = False)
  created_on = models.DateField( ("Date"), auto_now_add=True, blank=False )

  def __str__(self):
    return self.page_name

  class Meta:
    verbose_name = "Facebook Page"
    verbose_name_plural = "Facebook Pages"


class instagram(models.Model):
  CHOICES_CATAGORY  = (('AM', 'Arts Marketing'),('EP', 'Event Planning'),)
  handle   = models.CharField(max_length= 100, blank=False) 
  account_name = models.CharField(max_length= 100, blank=False)
  url 	  = models.CharField(max_length= 100, blank=False)  
  catagory  = models.CharField(max_length= 2, choices=CHOICES_CATAGORY, blank=True)
  description = models.TextField(default=True, blank = True)
  remarks = models.TextField(default = False, blank = True)
  is_active = models.BooleanField(default=False, blank = False)

  def __str__(self):
    return self.account_name

  class Meta:
    verbose_name = "Instagram Account"
    verbose_name_plural = "Instagram Accounts"	


class twitter(models.Model):
  CHOICES_CATAGORY  = (('AM', 'Arts Marketing'),('EP', 'Event Planning'),)
  handle   = models.CharField(max_length= 100, blank=False) 
  account_name = models.CharField(max_length= 100, blank=False)	
  url 	  = models.CharField(max_length= 100, blank=False)  
  catagory  = models.CharField(max_length= 2, choices = CHOICES_CATAGORY, blank = True)
  description = models.TextField(default=True, blank = True)
  remarks = models.TextField(default = False, blank = True)
  is_active = models.BooleanField(default=False, blank = False)

  def __str__(self):
    return self.account_name

  class Meta:
    verbose_name = "Twitter Handle"
    verbose_name_plural = "Twitter Handles"	


class youtube_videos(models.Model):
  SPAM_LEVEL = (
    ('NA','None'),
    ('TN','Thumbnail'),
    ('MT','Meta'),
    ('CM','Comma'),
    ('ML','Multiple'),
  )

  VIDEO_STATUS = (
    ("PR","private"),
    ("PB","public"),
    ("PL","published"),
  )

  channel_id_fk = models.ForeignKey(channel, blank=False, verbose_name="Select Channel", on_delete=models.CASCADE)
  video_id = models.CharField(max_length=30, blank=False, verbose_name="Video ID As In Youtube")
  video_title = models.CharField(max_length=250, blank=False, verbose_name="Video Title")
  thumbnail = models.CharField(max_length=50, default="", blank=True, verbose_name="Thumbnail URL")
  video_description = models.TextField(default=False, blank=False, verbose_name="Video Description")
  video_tags = models.TextField(default=False, blank=False, verbose_name="Video Tags")
  video_status = models.CharField( max_length = 2, choices = VIDEO_STATUS, blank=False, verbose_name="Video Status")
  video_published_at = models.DateTimeField( default=datetime.now, blank=True, verbose_name="Video Published Time")
  spam_level = models.CharField( max_length = 2, choices = SPAM_LEVEL, default='NA', blank=True )
  qc_action = models.BooleanField( default=False, blank=True )

  def __str__(self):
    return "%s" % (self.video_title)

  class Meta:
    verbose_name="Youtube Video"
    verbose_name_plural = "Youtube Videos"


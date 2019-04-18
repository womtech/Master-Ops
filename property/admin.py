# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from property.models import channel, cms, facebook, instagram, twitter, youtube_videos

# Register your models here.
class cmsAdmin( admin.ModelAdmin ):
  search_fields = ('cms_name','cms_id',)
  list_display = ('cms_id','cms_name','is_active')
  list_filter = ('cms_name','cms_id',)

class channelAdmin( admin.ModelAdmin ):
  search_fields = ('channel_name','is_active')
  list_display = ('channel_id','channel_name','is_Affiliate_Channel','is_active','remarks')
  list_filter = ('channel_name','is_active')

class facebookAdmin( admin.ModelAdmin ):
  search_fields = ('page_id','page_name')
  list_display = ('id','page_id','page_name','url','catagory','sub_catagory','tags','description','remarks','is_active')
  list_filter = ('page_name','catagory')

class instagramAdmin( admin.ModelAdmin ):
  search_fields = ('handle','account_name')
  list_display = ('id','handle','account_name','url','catagory','description','remarks','is_active')
  list_filter = ('handle','catagory')

class twitterAdmin( admin.ModelAdmin ):
  search_fields = ('partner_name','custom_id','genre')
  list_display = ('handle','account_name','url','catagory','description','remarks','is_active')
  list_filter = ('catagory','is_active')

class youtube_videosAdmin( admin.ModelAdmin ):
  search_fields = ('video_id','video_title')
  list_display = ('id','video_id','video_title','thumbnail','video_description','video_tags','video_status','spam_level','qc_action')
  list_filter = ('spam_level','qc_action')

admin.site.register( cms, cmsAdmin )
admin.site.register( channel, channelAdmin )
admin.site.register( facebook, facebookAdmin )
admin.site.register( instagram, instagramAdmin )
admin.site.register( twitter, twitterAdmin )
admin.site.register( youtube_videos, youtube_videosAdmin )

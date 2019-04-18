from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse, request

#import Asset
#from asset.models import music, album, title
from libraries.PostgreSQLConnector import PostgreSQLConnector
from django.http.response import JsonResponse
from django.core import serializers
import json


class MusicHome( View ):
  def get(self, request, *args, **kwargs):
      self.psy = PostgreSQLConnector()
      QUERY_SUMMARY = '''Select count(Distinct(a.album_id)) as Total_Albums, sum(a.acquisition_cost) as Total_acquisition_cost, count(distinct(a.title_id))  as Total_Music_Tracks from
	(SELECT aa.album_name, aat.album_id, at.acquisition_cost, aat.title_id from asset_title as at 
	join generic_asset_type as gat on at.type_id = gat.asset_id
	join asset_album_titles as aat on aat.title_id = at.id 
	join asset_album as aa on aa.id = aat.album_id where gat.asset_type ~ 'Track') as a'''
      response_summary = self.psy._custom(QUERY_SUMMARY, "select", "named_tuple")
      QUERY_ALBUM_SUMMARY = '''SELECT aa.album_name, aat.album_id, count(aat.title_id) as Total_Albums, floor(EXTRACT(EPOCH FROM current_timestamp-aa.added_on)/3600) as time_diff_hours from asset_title as at 
        join generic_asset_type as gat on at.type_id = gat.asset_id
        join asset_album_titles as aat on aat.title_id = at.id 
        join asset_album as aa on aa.id = aat.album_id where gat.asset_type ~ 'Track' group by aa.album_name, aat.album_id, aa.added_on order by aa.added_on desc
      '''
      recent_albums = self.psy._custom(QUERY_ALBUM_SUMMARY, "select", "named_tuple")
      QUERY_TRACK_SUMMARY = '''SELECT at.id, at.display_name, floor(EXTRACT(EPOCH FROM current_timestamp-at.added_on)/3600) as time_diff_hours
        from asset_title as at join generic_asset_type as gat on at.type_id = gat.asset_id where gat.asset_type ~ 'Track' order by at.added_on desc'''
      recent_tracks = self.psy._custom(QUERY_TRACK_SUMMARY, "select", "named_tuple")
      u = request.user.get_full_name
      return render(request, "onemusic/home.html", {'data': response_summary['data'], 'u': u, 'recent_albums': recent_albums, 'recent_tracks':recent_tracks})


class ReportsHome( View ):
  def get(self, request, *args, **kwargs):
    return render(request,"onemusic/reports.html")


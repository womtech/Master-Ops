
from django.shortcuts import render, redirect
from django.http import HttpResponse
from system.models import App, Apps_Assignment
from django.views.generic import TemplateView
from django.views.generic.base import View
from libraries.PostgreSQLConnector import PostgreSQLConnector

# Create your views here.

class Home( View ):

  def error_400( request ):
    return render( request, "home/error_400.html")

  def error_500( request ):
    return render( request, "home/error_500.html")


  def get(self,request,*args,**kwargs):
      USERNAME = str( request.user.id )
    #if request.session.is_empty():
    #  return redirect("authme/")
    #else:
      psy = PostgreSQLConnector(  )
      query = "select sa.name, sa.status, sa.about, sa.id, saa.profile_name, saa.description, sa.url from system_app sa \
        inner join system_apps_assignment saa on saa.app_id_fk_id=sa.id where saa.user_id_fk_id=" + USERNAME

      data = psy._custom( query,"select","named_tuple" )

      return render( request,"home/home.html", {'data':data } )


class MyItems( View ):

  def get(self, request, *args, **kwargs):
    return render( request, "home/my_items.html")

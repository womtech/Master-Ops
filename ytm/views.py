from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

# Create your views here.
class YTMHome ( View ):

  def get (self, request, *args, **kwargs):
    return render(request,"ytm/home.html")


class YTUpload ( View ):

  def get( self, request, *args, **kwargs ):
    return render( request, "ytm/upload.html")



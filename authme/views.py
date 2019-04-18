from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic.base import View
from libraries.PostgreSQLConnector import PostgreSQLConnector
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
import jwt, json


class Login( View ):

  #getLoggedIn User Info
  def getUserPayload(self):
    psy = PostgreSQLConnector( )
    query = "select sa.name, sa.status, sa.about, sa._id, saa.profile_name, saa.description from system_app sa \
         inner join system_apps_assignment saa on saa.app_id_fk_id=sa._id where saa.user_id_fk_id=2;"
    return psy._custom( query,"select","named_tuple" )



  def get( self, request ):
    username = request.GET.get("inputUsername",False)
    password = request.GET.get("inputPassword",False)

    if not username and not password:
      if request.session.test_cookie_worked():
        return render( request, "authme/login.html")
      else:
        return render( request, "authme/login.html", {"cookie_message":str(True)})

    if username and password:
      user = authenticate( username=username, password=password )
      if user is not None:
        if user.is_active:
          login( request, user )
          return self.postLogin( user.id, request  )
        else:
          messages.add_message( request, messages.INFO, 'Login Failed - Your Account Is Inactive', fail_silently=True)
          return render( request, 'authme/login.html'  )
      else:
        messages.add_message( request, messages.INFO, 'Login Failed - Please try again', fail_silently=True)
        return render( request, 'authme/login.html'  )
    #request.session.set_test_cookie( )
    #return render( request, "authme/login.html" )


  def postLogin( self, userID, request  ):
    response = HttpResponseRedirect('/')
    psy = PostgreSQLConnector( )
    query = '''select password from auth_user where id={} '''.format(userID)
    password_hash = psy._custom( query,"select")['data'][0][0]
    eToken = str( jwt.encode({'user_id':userID,'pswdhash':password_hash,'ip':request.META['REMOTE_ADDR'],'status':'is_actvie' }, "SECRET", algorithm="HS256"), 'utf-8')
    request.session['token'] = eToken
    request.session.modified = True
    response.set_cookie( "ctoken", eToken , max_age = 604800 )
    return response


  def logout( request ):
    response = HttpResponseRedirect("/authme/ccheck")
    response.delete_cookie("ctoken")
    logout( request )
    request.session.set_test_cookie()
    return response


  def ccheck( request ):
    response = HttpResponseRedirect("authme/")
    request.session.set_test_cookie()
    return response

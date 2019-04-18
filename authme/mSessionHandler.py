
# Middleware Class to Handle Session & JWT default operations
# Usage: Protect Function by mentioning @SessionHandler over the secured functions
# Written By: Thrinadh <thrinadh@wominternal.com>
# Date Written: Jan 1, 2019

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from libraries.PostgreSQLConnector import PostgreSQLConnector
from libraries.packages.Permissions import PagePermissions
import jwt


class SessionHandler( object ):

  '''
  Main Function to process request header authenticity
  Params: Object <request>
  Return Type: Object
  '''
  def process_request( self, request ):
    response = self.get_response( request )
    path = request.path_info
    PUBLIC_URLS = ('/authme/','/authme/ccheck')
    if path in PUBLIC_URLS:
      return response
    else:
      return self.regressChecking( request, path )

  def regressChecking( self, request, path ):
    response  = self.get_response( request )
    stoken = request.session.get('token', False)
    if 'ctoken' in request.COOKIES and stoken:
      if request.COOKIES['ctoken'] == stoken:
        if not path.startswith("/admin") and request.method != 'POST':
          return self.validatePagePermission( request, stoken, path )
        return response
    else:
        response_redirect = HttpResponseRedirect('/authme/')
        response_redirect.delete_cookie('csrftoken')
        response_redirect.delete_cookie('ctoken')
        return response_redirect


  def validatePagePermission( self, request, token, path ):
    if request.method == "GET":
      token_dump = jwt.decode( token , "SECRET", algorithms="HS256")
      userID = token_dump['user_id']
      status = self.validateUserPerm( path, userID )
      if status:
        return self.get_response( request )
      return HttpResponse("You are not allowed to access this page")


  def validateUserPerm( self, SLUG, USERID ):
    Obj = PagePermissions( SLUG, USERID )
    return Obj.is_page_permitted()

  def __init__( self, get_response ):
    self.get_response = get_response

  def __call__(self, request):
    response =  self.process_request(request)
    return response

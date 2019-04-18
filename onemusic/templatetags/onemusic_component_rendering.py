
from django import template
register = template.Library()

@register.inclusion_tag('onemusic/navbar.html', takes_context=True)
def getmenu( context, active_item ):
  user = context.request.user.get_full_name
  menus = [
    {"name": "Home", "url": "/onemusic/", "class":""},
    {"name": "Album", "url": "/admin/asset/album/", "class":""},
    {"name": "Title", "url": "/admin/asset/title/", "class":""},
    {"name": "Distributions", "url":"/admin/cfms/distribution/", "class":""},
    {"name": "Reports", "url":"/onemusic/reports/", "class":""},
  ]
  for menu in menus:
    if menu["name"] == str(active_item):
      menu["class"] = "active"
  return {'menus':menus, "user":user }


@register.inclusion_tag('onemusic/breadcrumb.html')
def getBreadCrumb( active_item ):
  available_bcrumbs = [{ "name":"Home","prop":[{"name":"Home","url":""}] }, { "name":"Reports", "prop":[{"name":"Home","url":"/onemusic/"},{"name":"Reports","url":''}]}]
  return {'breadcrumb': next(item for item in available_bcrumbs if item["name"] == active_item ) }


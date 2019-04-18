from django import template
register = template.Library()

@register.inclusion_tag('kpt/navbar.html', takes_context=True)
def getmenu( context, active_item ):
  user = context.request.user.get_full_name
  menus = [
    {"name": "Home", "url": "/kpt/", "class":""},
    {"name": "High CPC", "url": "/kpt/hcpc", "class":""},
    {"name": "Trending Keywords", "url": "/kpt/tcpc","class":""}
  ]
  for menu in menus:
    if menu["name"] == str(active_item):
      menu["class"] = "active"
  return {'menus':menus, "user":user }

@register.inclusion_tag('kpt/breadcrumb.html')
def getBreadCrumb( active_item ):
  available_bcrumbs = [{ "name":"Home","prop":[{"name":"Home","url":""}] }, { "name":"High Performing Keywords", "prop":[{"name":"Home","url":"/kpt/"},{"name":"High Performing Keywords","url":''}]},{ "name":"Trending Keywords", "prop":[{"name":"Home","url":"/kpt/"},{"name":"Trending Keywords","url":''}]}]
  return {'breadcrumb': next(item for item in available_bcrumbs if item["name"] == active_item ) }

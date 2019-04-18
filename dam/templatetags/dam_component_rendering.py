from django import template
register = template.Library()

@register.inclusion_tag('dam/navbar.html', takes_context=True)
def getmenu( context, active_item ):
  user = context.request.user.get_full_name
  menus = [
    {"name": "Home", "url": "/dam/", "class":""},
    {"name": "Lookups", "url": "/dam/lookups", "class":""},
  ]
  for menu in menus:
    if menu["name"] == str(active_item):
      menu["class"] = "active"
  return {'menus':menus, "user":user }

@register.inclusion_tag('dam/breadcrumb.html')
def getBreadCrumb( active_item ):
  available_bcrumbs = [{ "name":"Home","prop":[{"name":"Home","url":""}] }, { "name":"Lookups", "prop":[{"name":"Home","url":"/dam/"},{"name":"Lookups","url":''}]}]
  return {'breadcrumb': next(item for item in available_bcrumbs if item["name"] == active_item ) }

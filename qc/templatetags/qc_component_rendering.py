from django import template
register = template.Library()

@register.inclusion_tag('qc/navbar.html', takes_context=True)
def getmenu( context, active_item ):
  user = context.request.user.get_full_name
  menus = [
    {"name": "Home", "url": "/qc/", "class":""},
    {"name": "Videos", "url": "/qc/list", "class":""},
  ]
  for menu in menus:
    if menu["name"] == str(active_item):
      menu["class"] = "active"
  return {'menus':menus, "user":user }

@register.inclusion_tag('qc/breadcrumb.html')
def getBreadCrumb( active_item ):
  available_bcrumbs = [{ "name":"Home","prop":[{"name":"Home","url":""}] }, { "name":"Videos", "prop":[{"name":"Home","url":"/qc/"},{"name":"Videos","url":""}]} ]
  return {'breadcrumb': next(item for item in available_bcrumbs if item["name"] == active_item ) }

from django import template
register = template.Library()

@register.inclusion_tag('home/navbar.html', takes_context=True)
def getmenu( context, active_item ):
  user = context.request.user.get_full_name
  menus = [
    {"name": "Home", "url": "/", "class":""},
    {"name": "My Items", "url": "/myitems/", "class":""},
  ]
  for menu in menus:
    if menu["name"] == str(active_item):
      menu["class"] = "active"
  return {'menus':menus, "user":user }



from django import template
register = template.Library()

@register.inclusion_tag('cfms/navbar.html', takes_context=True)
def getmenu( context, active_item ):
  user = context.request.user.get_full_name
  menus = [
    {"name": "Home", "url": "/cfms/", "class":""},
    {"name": "Partners", "url": "/admin/extras/partner/", "class":""},
    {"name": "Contracts", "url": "/admin/cfms/contract/", "class":""},
  ]
  for menu in menus:
    if menu["name"] == str(active_item):
      menu["class"] = "active"
  return {'menus':menus, "user":user }

@register.inclusion_tag('cfms/breadcrumb.html')
def getBreadCrumb( active_item ):
  available_bcrumbs = [
    {"name":"Contract Report Detail","prop":[{"name":"Home","url":"/cfms/"},{"name":"Contract Performance Report","url":"/cfms/contract_performance"},{"name":"Contract Report Detail","url":""}]}, 
    {"name":"Contract Performance Report","prop":[{"name":"Home","url":"/cfms/"},{"name":"Contract Performance Report","url":""}]}, 
    {"name":"Platform Performance Report","prop":[{"name":"Home","url":"/cfms/"},{"name":"Platform Performance Report","url":""}]}, 
    {"name":"Asset Performance Report","prop":[{"name":"Home","url":"/cfms/"},{"name":"Asset Performance Report","url":""}]}, 
    {"name":"Partner Performance Report","prop":[{"name":"Home","url":"/cfms/"},{"name":"Partner Performance Report","url":""}]}, 
    {"name":"Home","prop":[{"name":"Home","url":""}] }, { "name":"Videos", "prop":[{"name":"Home","url":"/qc/"},{"name":"Videos","url":""}]} 
]
  return {'breadcrumb': next(item for item in available_bcrumbs if item["name"] == active_item ) }

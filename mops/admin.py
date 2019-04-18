from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

class MopsAdmin( AdminSite ):
  site_title = ugettext_lazy('Master Ops Dashboard')

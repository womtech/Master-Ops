from django.contrib import admin
from .models import Apps_Assignment, App, App_Form, User_Form_Level_Permission

# Register your models here.

class App_FormAdmin ( admin.ModelAdmin ):
  list_display = ('form_verbose','form_type','form_name_html','available_operations','search','filter','is_active')
  list_filter = ('app_id_fk',)

class AppAdmin( admin.ModelAdmin ):
  search_fields = ('name','url')
  list_display = ('name','about','url','theme','status')
  list_filter = ('theme','status')

class Apps_AssignmentAdmin( admin.ModelAdmin ):
  search_fields = ('profile_name','description')
  list_display = ('profile_name','description')
  list_filter = ('profile_name','description')

class User_Form_Level_PermissionAdmin( admin.ModelAdmin ):
  list_display = ("code","form_url","app_assignment_id_fk","form_type","full_privilege_on")
  list_filter = ("form_id_fk","form_type")

admin.site.register( App, AppAdmin )
admin.site.register( Apps_Assignment, Apps_AssignmentAdmin )
admin.site.register( App_Form, App_FormAdmin )
admin.site.register( User_Form_Level_Permission, User_Form_Level_PermissionAdmin )

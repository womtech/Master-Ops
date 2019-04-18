from django.contrib import admin
from .models import Genres_List, Business_Bucket, Asset_Type, Department, Language, Platform, Tag, Association_Type, Contract_Type

# Register your models here.
admin.site.register([Genres_List, Business_Bucket, Asset_Type, Department, Language, Platform, Tag, Association_Type, Contract_Type])

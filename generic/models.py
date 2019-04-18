# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models


# Create your models here.
class Genres_List(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=60, blank=False, unique=True)
    added_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.genre_name;

    class Meta:
        verbose_name = "Genre List"
        verbose_name_plural = "Genres List"


class Business_Bucket(models.Model):
    bucket_id = models.AutoField(primary_key=True)
    bucket_name = models.CharField(max_length=80, blank=False, unique=True)

    def __str__(self):
        return self.bucket_name

    class Meta:
        verbose_name = "Business Bucket"
        verbose_name_plural = "Business Buckets"


class Asset_Type(models.Model):
    asset_id = models.AutoField(primary_key=True)
    asset_type = models.CharField(max_length=80, blank=False, unique=True)

    def __str__(self):
        return self.asset_type

    class Meta:
        verbose_name = "Asset Type"
        verbose_name_plural = "Asset Types"


class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=80, blank=False, unique=True)

    def __str__(self):
        return self.dept_name

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"


class Language(models.Model):
    lang_id = models.AutoField(primary_key=True)
    language_name = models.CharField(max_length=60, blank=False, unique=True)

    def __str__(self):
        return self.language_name

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"


class Platform(models.Model):
    plat_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(max_length=70, blank=False, unique=True)

    def __str__(self):
        return self.platform_name

    class Meta:
        verbose_name = "Platform"
        verbose_name_plural = "Platforms"


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.tag_name


class Association_Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.name

class Contract_Type(models.Model):
    prefix = models.CharField(default=None, blank = True, max_length=50, unique=True)
    main_category = models.CharField(default=None, blank = False, max_length=50)
    sub_category = models.CharField(default=None, blank = True, max_length=50)

    def __str__(self):
       return self.prefix

    class Meta:
       verbose_name = "Contract Type"
       verbose_name_plural = "Contract Type"

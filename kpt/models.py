from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date

# Create your models here.
class Hcpc(models.Model):
  keyword = models.CharField(max_length=200, blank=False)
  volume = models.FloatField(null=True, blank=True, default=None )
  keyword_difficulty = models.FloatField( null=True, blank=True, default=None  )
  cost_per_click = models.FloatField( null=True, blank=True, default=None  )
  competitive_density = models.FloatField( null=True, blank=True, default=None )
  results = models.FloatField( null=True, blank=True, default=None )
  serp_features = models.CharField( max_length=200, blank=True)
  date = models.DateField( blank=True, default=date.today)

  def __str__(self):
    return "%s" % self.keyword

  class Meta:
    verbose_name = "High Performing Keyword"
    verbose_name_plural = "High Performing Keywords"

# Create your models here.
class TrendingKeywords(models.Model):
  keyword = models.CharField(max_length=200, blank=False)
  volume = models.FloatField(null=True, blank=True, default=None )
  keyword_difficulty = models.FloatField( null=True, blank=True, default=None  )
  cost_per_click = models.FloatField( null=True, blank=True, default=None  )
  competitive_density = models.FloatField( null=True, blank=True, default=None )
  results = models.FloatField( null=True, blank=True, default=None )
  serp_features = models.CharField( max_length=200, blank=True)
  date = models.DateField( blank=True, default=date.today)

  def __str__(self):
    return "%s" % self.keyword

  class Meta:
    verbose_name = "Trending Keyword"
    verbose_name_plural = "Trending Keywords"




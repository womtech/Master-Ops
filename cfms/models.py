from __future__ import unicode_literals
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import date
from extras.models import Partner, Contact
from generic.models import Platform
from asset.models import Title
from extras.models import FExchange
from generic.models import Contract_Type
from djmoney.models.fields import MoneyField
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class IPRight( models.Model ):
  def get_autogenerated_code():
    last_id = IPRight.objects.values('id').order_by('id').last()
    if not last_id:
      return "RIGHT-"+str(1)
    return "RIGHT-"+str(last_id['id'])

  right_type_option = (
    ('Both','Exclusive & Non Exclusive'),
    ('Excl','Exclusive'),
    ('NExc','Non Exclusive')
  )
  code = models.CharField( max_length = 20, default=get_autogenerated_code, editable=False)
  entity = models.CharField( max_length = 100, blank=False )
  right_type = models.CharField( max_length = 30, choices=right_type_option, default='Both', null=False, blank=False)
  exclusivity = models.CharField( max_length=100, blank=False, default="None" )
  inclusivity = models.CharField( max_length=100, blank=False, default="All" )

  def __str__(self):
    return "%s" % (self.code)

  class Meta:
    verbose_name = "IP Right"


class IPRightGroup (models.Model):
  def get_autogenerated_code():
    last_id = IPRightGroup.objects.values('id').order_by('id').last()
    if not last_id:
      return "RGRP-"+str(1)
    return "RGRP-"+str(last_id['id'])
  code = models.CharField( max_length = 20, default=get_autogenerated_code, editable=False)
  ip_right = models.ManyToManyField( IPRight, blank=False, null=False )

  def __str__(self):
    return "%s" % (self.code)

  class Meta:
    verbose_name = "IP Rights Group"


class Contract(models.Model):
    def get_autogenerated_code():
        last_id = Contract.objects.values('id').order_by('id').last()
        if not last_id:
            return "CT/" + str(1)
        return "CT/" + str(last_id['id'])
    code = models.CharField(max_length=10, default=get_autogenerated_code, editable=False, blank=False)
    nature = models.ForeignKey(Contract_Type, null=True, blank=False, verbose_name="Contract Nature", on_delete=models.CASCADE)
    sign_date = models.DateField(blank = False, default = date.today, verbose_name="Sign Date")
    start_date = models.DateField(blank = False, default = date.today, verbose_name="Start Date")
    end_date = models.DateField(blank = False, default = date.today, verbose_name="End Date")
    perpetual = models.BooleanField( default = False, blank = False )
    rights_group = models.ForeignKey( IPRightGroup, null=True, on_delete=models.CASCADE, related_name = "contract_associated_ip_rights_group")
    notes = models.TextField(blank=True, max_length=250, default=None)
    attach = models.FileField(blank=True)
    contract_status_option = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Draft', 'Draft'),
    )
    contract_status = models.CharField(max_length=15, choices=contract_status_option, default='Draft', null=False, blank=False )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contract"

class Contract_Signatories(models.Model):
    def get_autogenerated_code():
        last_id = Contract_Signatories.objects.values('id').order_by('id').last()
        if not last_id:
            return "CT/SG/" + str(1)
        return "CT/SG/" + str(last_id['id'])
    code = models.CharField(max_length=8, default=get_autogenerated_code, editable=False, blank=False)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    rev_percentage = models.IntegerField(default=0, verbose_name='Revenue Percentage', validators = [MinValueValidator(0), MaxValueValidator(100)] )
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    signer = models.TextField(default='', verbose_name="Signer Information", max_length=50, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Contract Signatory"
        verbose_name_plural = "Contract Signatories"



# Create your models here.
class Earning(models.Model):
  def get_autogenerated_code():
    last_fxchange_id = Earning.objects.values('id').order_by('id').last()
    if not last_fxchange_id:
      return "GR/ERN-"+str(1)
    return "GR/ERN-"+str(last_fxchange_id['id'])
  code = models.CharField( max_length = 20, default=get_autogenerated_code, editable=False)
  title_id = models.ForeignKey(Title, null=False, on_delete =models.CASCADE, related_name="earning_for_title")
  platform_id = models.ForeignKey(Platform, null=False, on_delete =models.CASCADE, related_name="earning_from_platform_for_title")
  contract = models.ForeignKey( Contract, null=False, on_delete=models.CASCADE, related_name="earning_for_contract")
  month = models.DateField( blank = False, default= date.today, verbose_name="Earning For Month")
  revenue = MoneyField(max_digits=10, decimal_places=2,verbose_name="Gross Revenue", default_currency= "USD")
  currency = models.ForeignKey(FExchange, null=False, on_delete =models.CASCADE, related_name="earning_in_currency" )

  def __str__ (self):
    return "%s" % (self.code)

  class Meta:
    verbose_name="Earning"
    verbose_name_plural = "Earnings"
    unique_together = ('title_id', 'platform_id', 'month','contract')


class EarningSplit( models.Model ):
  def get_autogenerated_code():
    last_id = EarningSplit.objects.values('id').order_by('id').last()
    if not last_id:
      return "ERN/SPLIT-"+str(1)
    return "ERN/SPLIT-"+str(last_id['id'])
  code = models.CharField( max_length = 20, default=get_autogenerated_code, editable=False)
  earning_ref = models.ForeignKey( Earning, null=False, on_delete=models.CASCADE, related_name="earning_correspondence" )
  partner = models.ForeignKey( Partner, null=False, on_delete=models.CASCADE, related_name="earning_split_for_partner" )
  calculated_revenue_usd = models.FloatField( null=False, blank=False, default=0.0 )

  def __str__ (self):
    return "%s" % (self.code)

  class Meta:
    verbose_name="Earning Split"
    verbose_name_plural = "Earning Splits"
    unique_together = ('earning_ref', 'partner')




class Distribution(models.Model):
  def get_autogenerated_code():
    last_id = Distribution.objects.values('id').order_by('id').last()
    if not last_id:
      return "DSTR-"+str(1)
    return "DSTR-"+str(last_id['id'])
  code = models.CharField( max_length = 20, default=get_autogenerated_code, editable=False)
  contract = models.ForeignKey( Contract, null=False, blank=False, related_name="distributed_under_contract", on_delete=models.CASCADE)
  platform    = models.ForeignKey(Platform, null=False, related_name="distributed_on_platform", on_delete= models.CASCADE)
  title       = models.ForeignKey(Title, null=False, related_name="this_title_distributed",  on_delete=models.CASCADE)
  remark      = models.TextField(max_length = 50, blank= True)
  distributed_on = models.DateField(default=date.today, blank=False)

  def __str__ (self):
    return "%s" % (self.code)

  class Meta:
    verbose_name = "Distribution"
    verbose_name_plural = "Distributions"



@receiver(post_save, sender = Earning)
def SplitEarningsSignal(sender, instance, created, **kwargs):
  cso = Contract_Signatories.objects.filter(contract=instance.contract)
  for j in cso:
    grossRevenue, partnr =  (instance.revenue*j.rev_percentage)/100, j.partner
    if created:
      EarningSplit.objects.create(calculated_revenue_usd=grossRevenue, partner = partnr, earning_ref=instance)

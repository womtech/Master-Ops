from django.db import models
from django.conf import settings
from property.models import cms, channel, facebook, instagram, twitter
from cfms.models import Contract

# Create your models here.

class property_ownership( models.Model ):

    id = models.AutoField( primary_key=True)
    user_id_fk = models.ForeignKey( settings.AUTH_USER_MODEL, default=1, verbose_name="Select User", blank=False, on_delete=models.CASCADE )
    cms_name_id_fk = models.ManyToManyField( cms )
    channel_name_id_fk = models.ManyToManyField( channel )
    facebook_page_id_fk = models.ManyToManyField( facebook )
    instagram_account_name_id_fk = models.ManyToManyField( instagram )
    twitter_account_name_id_fk = models.ManyToManyField( twitter )
    contract_id_fk = models.ManyToManyField( Contract  )

    def __str__ ( self ):
        return "%s" % (self.user_id_fk)

    class Meta:
        verbose_name="Property_ownership"
        verbose_name_plural="Property_ownership"


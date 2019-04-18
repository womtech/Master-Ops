from django.db import models
from property.models import channel
from django.conf import settings

# Create your models here.
class ytm_upload_track(models.Model):
  id = models.AutoField( primary_key=True , blank=False )
  channel_id = models.ForeignKey(channel, blank=False, verbose_name="Select Channel", on_delete=models.CASCADE)
  track = models.CharField(max_length=200, blank=False, verbose_name="Video Title")
  uploader_id = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE )

  def __str__(self):
    return self.track

  class Meta:
    verbose_name = "Upload Track"
    verbose_name_plural = "Upload Tracks"

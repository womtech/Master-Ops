from django.db import models
from property.models import youtube_videos
from django.contrib.auth.models import User
# Create your models here

class qclog(models.Model):
  id = models.AutoField( primary_key = True )
  video_id = models.ForeignKey( youtube_videos, default = 1, on_delete=models.CASCADE )
  moderator_remark = models.CharField( max_length = 255, default="None", blank=True, verbose_name="Moderator's Remark" )
  remark_from = models.ForeignKey( User, related_name="qclog_remark_from", default = 1, on_delete=models.CASCADE)
  qced_by  = models.ForeignKey( User, related_name='qclog_qced_by', default=1, on_delete=models.CASCADE )
  qced_on = models.DateTimeField( auto_now_add=True )
  qc_status = models.BooleanField( default=False, blank=True )

  def __str__(self):
    return str(self.video_id)

  class Meta:
    verbose_name = "QC Log"
    verbose_name_plural = "QC Logs"

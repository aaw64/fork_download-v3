from django.db import models
import os

# Create your models here.
class DownloadFile(models.Model):
    url = models.CharField(max_length= 255 , unique = True)
    path = models.CharField(max_length= 255)
    
    def hit_count(self):
        return DownloadRecord.objects.filter(file=self).count()

    def basename(self):
        return os.path.basename(self.url)

    def is_valid(self):
        # returns True if path exists on disk, is a file and is readable
        if os.path.exists(self.path) and os.path.isfile(self.path) and os.access(self.path , os.R_OK):
            return True
        else:
            return False
       
class DownloadRecord(models.Model):
    file = models.ForeignKey(DownloadFile,null=True)
    client_ip = models.CharField(max_length=32)
    client_email = models.CharField(max_length = 255, default='anonymous')
    timestamp = models.DateTimeField(auto_now_add=True)

    

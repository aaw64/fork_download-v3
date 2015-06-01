from .models import DownloadFile, DownloadRecord
from django.http import HttpRequest 
#from django.contrib.auth.models import User 
import os
class FileRegistry(object):
    def __init__(self):
        pass

    def get_file(self,request):
        return FileWrapper(request)

    def register_file(self , url, path, overwrite=False):
        # create a download file
        f = open(path,'w')
        f.write("Hello")
        f.close()
        return True        

class FileWrapper(object):
    def __init__(self,request):
        self.request = request
        url = request.path           # request.path
        try:
            self.file_obj = DownloadFile.objects.get(url=url)
        except DownloadFile.DoesNotExist:
            self.file_obj = None#DownloadFile()  # this should be none


    def is_valid(self):
        # file_obj exists and path exists on disk, path is a file and is readable
        request = self.request
        url = request.path 
        file_obj = self.file_obj
        if file_obj is not None and os.path.exists(url) and os.path.isfile(url) and os.access(url , os.R_OK):
            return file_obj.is_valid()
        else:
            return False

    def record_hit(self):
        # create a DownloadRecord for file_wrapper.file_obj
        request = self.request
        file_obj = self.file_obj
        record = DownloadRecord()
        record.file = file_obj
        record.client_ip = request.META.get('REMOTE_ADDR')
        #user = User.objects.get(id=1)
        if  request.user.is_active == 'TRUE':
            record.client_email = request.user.email
        else:
            record.client_email = "anonymous" 
        record.timestamp = request.user.timestamp
        return record
 
    def send_file(self):
        request = self.request
        from sendfile import sendfile
        # use sendfile library to send file_wrapper.file_obj
        # make it an attachment with attachment name file_wrapper.file_obj.basename()
        #file_wrapper = FileWrapper(self.request)
        file_obj = self.file_obj      
        return sendfile(request,file_obj.basename(),attachment=True,attachment_filename=file_obj.basename())            

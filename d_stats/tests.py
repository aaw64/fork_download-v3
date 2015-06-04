"""

Dada
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone
from models import DownloadFile, DownloadRecord
from .helpers import FileRegistry , FileWrapper
from django.http import HttpRequest , HttpResponse , Http404
from django.test.client import Client 
from django.conf import settings
import mock
import os

class Download_StatsTest(TestCase):    
    def create_downloadfile(self, url='user/download/temp.file', path= '/web/development/eddy_flux/src/download_stats/temp.file'):
        """
            creates DoownloadFile record with url = 'user/download/temp.file' , path = '/web/development/eddy_flux/src/download_stas/temp.file'
        """
        return DownloadFile.objects.create(url = url , path = path )

    def test_downloadfile_creation(self):
        """
           checks whether an instance of DownloadFile is created
        """
        d = self.create_downloadfile()
        self.assertTrue(isinstance(d,DownloadFile))


    def create_downloadrecordfile(self,client_ip= '192.23.332.112', client_email='abi@gmail.com', timestamp = '19:233'):
        """
               creates a DownloadRecord object
        """
        return DownloadRecord.objects.create(file = self.create_downloadfile() , client_ip = client_ip , client_email = client_email , timestamp = timestamp )

    def test_downloadrecord_creation(self):
        """
             checks whether an instance of DownloadRecord is created
        """
        d_record = self.create_downloadrecordfile()
        self.assertTrue(isinstance(d_record,DownloadRecord))

    def test_downloadfile_count(self):
        """
             checks the count of DownloadFile objects
        """
        d = self.create_downloadfile()
        c = DownloadFile.objects.filter(id = d.id).count()
        self.assertEqual(c,1)

    def test_downloadfile_hit_count(self):
        """
             checks the number of DownloadRecord created 
        """
        d = self.create_downloadfile()
        dr_obj = DownloadRecord()
        dr_obj.file = d
        dr_obj.save()
        self.assertEqual(d.hit_count(),1)       

    def test_downloadfile_basename(self):
        """
              checks the basename of the DownloadFile
        """
        d = self.create_downloadfile()
        self.assertEqual(d.basename(),'temp.file')
        #self.assertEqual(d_obj.basename(),'user/download/temp.file')

    def test_downloadfile_is_valid(self):
        """
               checks whether the download file exists on disk , is a file and readable
        """
        d_obj = DownloadFile() 
        d_obj.path = '/web/development/eddy_flux/src/download_stats/temp.file'
        self.assertEqual(d_obj.is_valid(),False)
     

    def test_downloadfile_not_valid(self):
        """
               checks for the condition downloadfile not valid
        """
        d_obj = DownloadFile()
        d_obj.path = "/web/temp.file"
        self.assertEqual(d_obj.is_valid(),False)
    

    def test_FileWrapper(self):
        """
             checks whether an instance of FileWrapper is created
        """
        request = HttpRequest()
        request.path = 'user/download/temp.file'
        d_obj = self.create_downloadfile()
        fw_obj = FileWrapper(request=request)
        #fw_obj.file_obj =  DownloadFile.objects.get( url = request.path )
        self.assertTrue(isinstance(fw_obj,FileWrapper)) 

    def test_FileWrapper_is_valid(self):
        """
            check whether a Filewrapper.file_obj exists and is_valid()
        """
        request = HttpRequest()
        request.url = 'user/download/temp.file' 
        request.path ='/web/development/eddy_flux/src/download_stats/temp.file'
        f = FileWrapper(request=request) 
        d = self.create_downloadfile()
        f.file_obj =  DownloadFile.objects.get(url = request.url )
        self.assertEqual(f.is_valid(),False)
        

    def test_FileWrapper_record_hit(self):
        """
             checks whether a FileWrapper creates a DownloadRecord 
        """
        #d_record = self.create_downloadfile() 
        r = mock.Mock()
        r.user.email = "abi@gmail.com"
        r.user.is_active = "True"
        r.url = "user/download/temp.file"
        r.path = '/web/development/eddy_flux/src/download_stats/temp.file'
        r.META.REMOTE_ADDR = "122.373.33.22" 
        f = FileWrapper(request=r)
        d_file=self.create_downloadfile()
        f.file_obj = DownloadFile.objects.get(url = r.url ) 
        #self.assertTrue(isinstance(f.record_hit(),DownloadRecord))
         
    def test_FileWrapper_send_file(self):
        """
            checks Filewrapper.send_file
        """
        settings.SENDFILE_BACKEND = 'sendfile.tests'
        from sendfile import sendfile
        request = HttpRequest() 
        request.url = 'user/download/temp.file'
        f_wrapper = FileWrapper(request=request)
        d_file = self.create_downloadfile()
        f_wrapper.file_obj =  DownloadFile.objects.get( url = request.url)
        #self.assertTrue(isinstance(f_wrapper.send_file(), HttpResponse))
        

    def test_FileRegistry_get_file(self):
        """
            chechs FileRegistry.get_File returns FileWrapper
        """
        request = HttpRequest()
        f_register = FileRegistry()
        self.assertTrue(isinstance(f_register.get_file(request),FileWrapper))        


    def test_FileRegistry_register_file(self):
        """
             check whether a download file is created
        """
        f_register = FileRegistry()
        #self.assertEqual(f_register.register_file('user/download/te.file','te3.file',False),os.path.isfile('te3.file') )

    def test_view_download_file(self):
        """
               checks whether a view download file is returns Http404
        """
        from . import views
        request = HttpRequest()
        url = 'user/download/temp.file'
        #request.path = '/web/development/eddy_flux/src/download_stats/temp.file'   
        f_wrapper = FileWrapper(request)
        d_file = self.create_downloadfile() 
        d_file.save()
        f_wrapper.file_obj =  DownloadFile.objects.get( url = url)
        #self.assertEqual(views.download_file(request = request),HttpResponse)  
        #import pdb
        #pdb.set_trace() 
        #self.assertRaises(views.download_file(request = request),Http404)
               
    def test_get_file_contents_DownloadFile(self):
        settings.SENDFILE_BACKEND = 'sendfile.tests'
        from sendfile import sendfile
        request = HttpRequest() 
        request.url = 'user/download/temp.file'
        f_wrapper = FileWrapper(request=request)
        d_file = self.create_downloadfile()
        f_wrapper.file_obj =  DownloadFile.objects.get( url = request.url)
        #response = f_wrapper.send_file()
        #self.assertEqual(response.content, 'temp.file')


































        
 




   


     


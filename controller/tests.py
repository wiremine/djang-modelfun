from django.test import TestCase
from django.test.client import Client
from django.core import mail
# mail.outbox will contain emails during tests
from django.http import HttpResponse
from django.core.urlresolvers import clear_url_caches
from django.conf import settings

from base import BlogController

blog_urls = (
    (r'^sample1/$', 'sample-1'),
    (r'^sample2/$', 'sample-2'),
    (r'^sample3/$', 'sample-3'),
    (r'^sample4/$', 'sample-4'),
)

def param_sample_view(request, delegate=None, url_name=None):
    return HttpResponse("Hello World")

views = {
    'sample-3': param_sample_view,
}


class ControllerTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_create_controller(self):
        blog_controller = BlogController(urls=blog_urls, views=views)

        settings.ROOT_URLCONF = blog_controller.get_urls()
        clear_url_caches()
        
        response = self.client.get('/sample1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Hello World From basestring")
        
        response = self.client.get('/sample2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Hello World")
        
        response = self.client.get('/sample3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Hello World")
        
        response = self.client.get('/sample4/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Hello World 4")
        
        
        
from django.test import TestCase
from django.test.client import Client
from django.core import mail
# mail.outbox will contain emails during tests
from django.http import HttpResponse
from django.core.urlresolvers import clear_url_caches
from django.conf import settings


class ControllerTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_controller_urls(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Hello World")

        response = self.client.get('/blog2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Hello World")
        

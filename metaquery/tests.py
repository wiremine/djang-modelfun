from django.test import TestCase
from django.test.client import Client
from django.core import mail
# mail.outbox will contain emails during tests

from datetime import datetime, timedelta
from models import Post, CustomPost

class MetaQueryTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_maker(self):
        publish_date = datetime.now() + timedelta(3)
        future_post = CustomPost(
            title="Future Post Title", 
            publish_on=publish_date, 
            publish=True, 
            content="Hello World"
        )
        future_post.save()
        
        today_post = CustomPost(
            title="Today Post Title", 
            publish_on=datetime.now(), 
            publish=True, 
            content="Hello World",
            featured=True
        )
        today_post.save()

        self.assertEqual(CustomPost.my_manager.count(), 2)

        self.assertEqual(len(CustomPost.my_manager.all().published()), 1)
        self.assertEqual(len(CustomPost.my_manager.published()), 1)

        self.assertEqual(CustomPost.my_manager.filter(title="Future Post Title")[0], future_post)
        qs = CustomPost.my_manager.all()
        self.assertEqual(
            qs.filter(title="Future Post Title")[0], 
            future_post)
            
        self.assertEqual(Post.my_manager.published().count(), 1)    
        qs = Post.my_manager.all()
        self.assertEqual(qs.published().count(), 1)
            
        self.assertEqual(len(CustomPost.my_manager.featured()), 1)
        qs = CustomPost.my_manager.all()
        self.assertEqual(qs.featured().count(), 1)    
            
            
            
            
            
            
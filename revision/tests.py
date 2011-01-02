from datetime import datetime

from django.test import TestCase
from django.test.client import Client
from django.core import mail
# mail.outbox will contain emails during tests

from revision.models import Post

from pymongo import Connection
from revision.utils import model_to_dict

class RevisionTestCase(TestCase):
    #fixtures = []
    #urls = ''

    def setUp(self):
        post = Post(title='Test Title', body="Hello World")
        post.save()
        connection = Connection()
        db = connection.revision_test_db
        self.collection = db.revisions
        
    def tearDown(self):
        self.collection.remove({})
        
    def test_serialize(self):
        post = Post.objects.select_related().all()[0]

        app_label = post._meta.app_label
        d = model_to_dict(post)

        # Figure out the newest migration, if we're using south
        try:
            from south.models import MigrationHistory
            migration_history = MigrationHistory.objects.filter(app_name=app_label).order_by('-applied')
            migration = migration_history[0].migration
        except:
            migration = None
            
        doc = {
            'record': d,
            'app_label': app_label,
            'timestamp': datetime.now(),
            'migration': migration, 
            'action': 'created' # created, modified, deleted
        }    
            
        self.collection.insert(doc)

        self.assertEqual(Post.objects.count(), 1)
        result = self.collection.find_one({'record.body': 'Hello World'})
        print result
        
        
        
        
        
        
        
from datetime import datetime

from django.test import TestCase
from django.test.client import Client
from django.core import mail
# mail.outbox will contain emails during tests

from revision.models import Post

from pymongo import Connection
from revision.utils import model_to_dict

from pprint import pprint

# TODO:
## Create mixin for admin to save this
## Handle inlines?
## Search revisions (using admin's search fields?)
## Show revisions?
  ## Created a read-only view?
## Restore? How to handle select_related fields? Restore and apply revisions?
## Cap the number of revisions per record?

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

        pprint(post._meta.fields)

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
            'model': post._meta.object_name.lower(), # TODO: be smarter about proxy
            'timestamp': datetime.now(),
            'migration': migration, 
            'action': 'created', # created, modified, deleted
            'admin': None # the admin who made the change
        }    
            
        self.collection.insert(doc)

        self.assertEqual(Post.objects.count(), 1)
        result = self.collection.find_one({'record.body': 'Hello World'})
        pprint(result)
        
        
        
        
        
        
        
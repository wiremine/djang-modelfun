from django.db import models
from django.db.models.manager import ManagerDescriptor
from django.utils.translation import ugettext_lazy as _
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes import generic
#from tinymce import models as tinymce_models
#from filebrowser.fields import FileBrowseField
from django.contrib.auth.models import User
from datetime import datetime
import inspect 

from manager_maker import manager_from

from types import ClassType
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
import inspect

class CustomManager(models.Manager):
    """
    A custom Manager class that automatically extends itself.
    
    At run-time it creates a new QuerySet class, with mixins from the manager's
    model object, and the model's super classes. It looks for an inner class called
    CustomQueries, and uses them as mixins for the new QuerySet. 
    
    For example:
    
        class MyModel(models.Model):
            custom_manager = CustomManager()
            class BaseQueries:
                def published(self):
                    return self.filter(published=True)

        qs = MyModel.custom_manager.all().published()

    published() ends up being a mixin to the QuerySet.
    
    The manager also automatically proxies method calls to the QuerySet object, too. 
    This enables you to execute the same custom queries on the manager directly. 
    
    For example:
    
        qs = MyModel.custom_manager.published()
    """
    # TODO: should Custom Queries live in the manager, too?
    my_queryset_class = None

    def _make_custom_manager(self):
        """
        Create a new QuerySet class with mixins found in the Manager's model
        and it's super classes.
        """
        if self.my_queryset_class == None:
            qs = super(CustomManager, self).get_query_set()
            bases = [QuerySet] # TODO: get this from the super class?

            for c in inspect.getmro(self.model):
                if hasattr(c, "CustomQueries") and isinstance(c, (ClassType, type)):
                    bases.append(c.CustomQueries)

            id = hash(tuple(bases))
            
            self.my_queryset_class = type('Queryset_%d' % id, tuple(bases), {})        

    # Proxy to the underlying queryset
    def __getattr__(self, attr):
        """Proxy to the underlying QuerySet object."""
        if self.my_queryset_class == None:
            self._make_custom_manager()
        qs = self.get_query_set()
        return getattr(qs, attr)

    def get_query_set(self):
        """Return the custom queryset."""
        if self.my_queryset_class == None:
            self._make_custom_manager()
        return self.my_queryset_class(self.model, using=self._db)


class Post(models.Model):
    """
    Example blog post
    """
    title = models.CharField(max_length=100)
    #user = models.ForeignKey(User)
    publish_on = models.DateField()
    publish = models.BooleanField(default=True)
    content = models.TextField(blank=True)
    featured = models.BooleanField(default=False)

    my_manager = CustomManager()
    
    class CustomQueries:
        def published(self):
            return self.filter(publish_on__lte=datetime.now())
            
class CustomPost(Post):
    
    last_name = models.CharField(blank=True, max_length=100)

    my_manager = CustomManager()

    class CustomQueries:
        def published_two(self):
            return self.filter(publish_on__lte=datetime.now())

        def featured(self):
            return self.filter(featured=True)
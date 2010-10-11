from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes import generic
#from tinymce import models as tinymce_models
#from filebrowser.fields import FileBrowseField

from app import get_model_label_by_role

class AbstractPerson(models.Model):
    """
    Hello World
    """
    first_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        abstract = True
        
class Person(AbstractPerson):
    pass
        

class Address(models.Model):
    """
    References a class
    """
    # TODO: What would South Do?
    person = models.ForeignKey(get_model_label_by_role('person', 'people.Person'))
    street1 = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return self.street1

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = []



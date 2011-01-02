from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes import generic
#from tinymce import models as tinymce_models
#from filebrowser.fields import FileBrowseField

class Category(models.Model):
    """
    Sample Category
    """
    name = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    """
    Sample blog post
    """
    title = models.CharField(blank=True, max_length=100)
    body = models.TextField(blank=True)
    timestamp = models.DateField(auto_now_add=True)
    sample_email = models.EmailField(blank=True, null=True)
    author = models.ForeignKey("auth.User", blank=True, null=True)

    def __unicode__(self):
        return "Post"

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-timestamp']



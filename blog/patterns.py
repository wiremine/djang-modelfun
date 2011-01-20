from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes import generic
#from tinymce import models as tinymce_models
#from filebrowser.fields import FileBrowseField

# We keep patterns separate from models so we can reuse patterns
# Across multiple apps.
class PostPattern(models.Model):
    """A Post Pattern"""
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    publish_on = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ['-publish_on']




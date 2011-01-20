from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes import generic
#from tinymce import models as tinymce_models
#from filebrowser.fields import FileBrowseField

from blog.patterns import PostPattern

class Post(PostPattern):
    pass


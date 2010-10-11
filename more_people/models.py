from django.db import models
from django.utils.translation import ugettext_lazy as _

from people.models import AbstractPerson

class PersonWithBio(AbstractPerson):
    """Another person class"""
    bio = models.TextField(blank=True)

    




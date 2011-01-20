from django.conf.urls.defaults import url
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponse        
from django.views.generic import TemplateView
        
class ModelLookupException(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message
        
# This is a mixin so we can mix it into custom M2M and KF fields        
class ModelRoleMixin(object):
    def get_model_label_by_role(self, role):
        """
        Return the app.model name for a model in django.conf.settings.MODELS

        If not present, returns fall_back.
        """
        # TODO:
        # role could have dots; if so, split by dot; the last element 
        # of the resulting array is the last key that should map 
        # to a app.model
        # The rest are keys of dicts within the settings.MODELS dict
        
        if not isinstance(settings.MODELS, dict):
            raise Exception("settings.MODELS should be a dict")

        if settings.MODELS.has_key(role):
            return settings.MODELS[role]
        else:
            return None
            
    def get_model(self, role):
        """
        Return the given class for the model
        """
        model_name = self.get_model_label_by_role(role)
        try:
            app_label, model_name = model_name.lower().split('.')
            model_type = ContentType.objects.get(app_label=app_label, model=model_name)
            return model_type.model_class()
        except:        
            raise ModelLookupException("Could not get class for role %s" % role) 

# TODO: the delgate might want to have a set of default model roles
# which then could be overwritten by the global settings.ROLES     
class Controller(ModelRoleMixin):
    """Base Controller"""

    urls = None
    views = {}
    templates = {}
    models = {}
    middleware = ()
    delegate = None # Thinking ahead, not used
        
    def __init__(self, urls=None, views=None, models=None, templates=None):
        """Customize the controller."""
        if urls:
            self.urls = urls
        self.additional_views = views
        self.additional_models = models
        self.additional_templates = templates

    @classmethod
    def as_urls(cls, urls=None, views=None, models=None, templates=None):
        instance = cls()
        return instance.get_urls()
    

    def combine_views(self):
        # Get the views from the parent, and merge them into
        # my views attribute.
        views = None
        for cls in reversed(self.__class__.__mro__):
            if hasattr(cls, 'get_views'):
                ancestor_instance = cls()
                views.update(ancestor_instance.get_views())
            elif hasattr(cls, 'views'):
                views.update(cls.views)
            else:
                views = {}

        if self.views:
            views.update(self.views)

        if self.additional_views:
            views.update(self.additional_views)

        return views
        
    def get_urls(self):
        """Generate a list of 'concrete' urls"""
        # Raise an error if self.urls is None
        pattern_list = []
        kwargs = {}
        kwargs['delegate'] = self # This is unneeded for delegate methods
        views = self.combine_views()
        for pattern in self.urls:
            regex = pattern[0]
            name = pattern[1]
            if name in views.keys():
                view = views[name]
            else:
                view = None # What do do here?
            kwargs['url_name'] = name
            t = url(regex, view, name=name, kwargs=kwargs, prefix='')
            pattern_list.append(t)
        return pattern_list 

    def get_template_name(self, url_name):
        """Get the template name"""
        if url_name in self.templates.keys():
            return self.templates[url_name]
        else:
            return None
            
    def __getattr__(self, role):
        """Helper function to make it easier to get a model"""
        return self.get_model(role)
        

class ControllerTemplateView(TemplateView):
    delegate = None
    url_name = None

class IntermediateController(Controller):        
    def get_views(self):
        return {
            'sample-1': 'controller.views.sample_view3',
            'sample-4': ControllerTemplateView.as_view(
                delegate=self, template_name='template_view_test.html') 
        }
        
def sample_view_2(request, delegate=None, url_name=None):
    return HttpResponse("Hello World")
        
class BlogController(IntermediateController):
    views = {
        'sample-2': sample_view_2,
    }
    templates = {'post-list': 'post_list.html'}
    models = {}
    

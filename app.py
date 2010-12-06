from django.conf import settings
from django.contrib.contenttypes.models import ContentType

# This smells a bit like Dependency Injection 
#    http://code.activestate.com/recipes/413268/

class ModelLookupException(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

def get_model_label_by_role(model_role, fall_back):
    """
    Return the app.model name for a model in django.conf.settings.MODELS
    
    If not present, returns fall_back.
    """
    if not isinstance(settings.MODELS, dict):
        raise Exception("settings.MODELS should be a dict")
    
    if settings.MODELS.has_key(model_role):
        return settings.MODELS[model_role]
    else:
        return fall_back
        
def get_model(model_role, fall_back):
    """
    Return the given class for the model
    """
    model_name = get_model_by_role(model_role, fall_back)
    try:
        app_label, model_name = model_name.lower().split('.')
        model_type = ContentType.objects.get(app_label=app_label, model=model_name)
        return model_type.model_class()
    except:        
        raise ModelLookupException("Could not get class for role %s or fall back %s" % (model_role, fall_back))
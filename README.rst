Experiments with decoupling Django components to make more reusable apps.

Ideally we can decouple with the thinnest glue/changes possible.

Experiment #1: Loosely Coupled Models
=====================================

The basic idea is this: look up models by their role in the application,
instead of calling them concretely. 

settings.MODELS is a dict where ['role': 'app_label.Model_name']

See app.py for the two methods that make this happen:

get_model_label_by_role() looks up a model by role, or uses the fall back. Returns a string of the format 'app_label.Model_name'. Not sure if we need the fall back: might be better to fail loudly if something is misconfigured. 

get_model() returns the model defined by the role.

ManyToManyFieldByRole('role or app.model')
 - should try looking up the role, or return the app.model name

Experiment #2: Model Extensions 
===============================
A model should look for "extensions" and load them at runtime. 

# Remove, add or change fields
# add mixins

people/
extensions/
  people/
     extension1/
        models.py
     extension2/
        models.py




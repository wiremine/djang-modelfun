from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail

def sample_view3(request, delegate=None, url_name=None):
    return HttpResponse("Hello World From basestring")
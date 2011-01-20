from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail

def homepage(request, delegate=None, url_name=None):

    posts = delegate.post.objects.all() 
    print posts
    
    # This should be much cleaner with class based views,
    # But can we clean this up for classic views, too?    
    template = delegate.get_template_name(url_name) 
    return render_to_response(template, {
    }, context_instance=RequestContext(request))

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from blog.controller import BlogController, blog_controller

urlpatterns = patterns('',
    ('^blog/', include(BlogController.as_urls())),
    ('^blog2/', include(blog_controller.get_urls()))
)

from modelfun.controller import Controller

class BlogController(Controller):
    urls = (
        (r'^$', 'blog-list'),
    )
    views = {
        'blog-list': 'blog.views.homepage'
    }
    templates = {
        'blog-list': 'post_list.html'
    }
    
blog_controller = BlogController() 
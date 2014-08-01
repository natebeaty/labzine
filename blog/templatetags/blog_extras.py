from django import template
from django.template import Library, Node, TemplateSyntaxError
from django.db.models import get_model
from labzine.blog.models import *
from labzine.tags.models import *
from labzine.articles.models import *
import datetime
     
register = Library()
     
class BlogVars(Node):
    def render(self, context):
        context['blog_month_list'] = Blog.objects.dates("date_added", "month")
        context['current_issue'] = Issue.objects.latest()
        context['tags_list'] = Tag.objects.filter(blog__id__isnull=False).distinct()
        context['foo'] = 'bar';
        return ''

def get_blog_vars(parser,token):
    return BlogVars()

get_blog_vars = register.tag(get_blog_vars)

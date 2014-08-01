from django.conf.urls.defaults import *
from labzine.tags.models import Tag
from labzine.articles.models import *
from labzine.blog.models import *
from labzine.blog.feeds import *

blog_dict = {
    'queryset': Blog.objects.all(),
    # 'template_object_name': 'blog',
    'date_field': 'date_added',
}
blog_date_dict = {
    'queryset': Blog.objects.all(),
    'template_object_name': 'blog',
    'date_field': 'date_added',
    'allow_future': 'true',
    'allow_empty': 'true',
}
blog_category_dict = {
    'queryset': Category.objects.all(),
    'template_object_name': 'category',
}

urlpatterns = patterns('',
    (r'^category/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(blog_category_dict, slug_field='slug')),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'django.views.generic.date_based.object_detail', dict(blog_dict, slug_field='slug',template_object_name='blog',allow_future='true',)),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$','django.views.generic.date_based.archive_day', blog_date_dict),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$','django.views.generic.date_based.archive_month', blog_date_dict),
    (r'^(?P<year>\d{4})/$','django.views.generic.date_based.archive_year', dict(blog_date_dict,make_object_list="true",)),  
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed'),
    (r'^$', 'django.views.generic.date_based.archive_index',dict(blog_dict, template_name="blog/blog_homepage.html")),
)
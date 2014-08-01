from django.conf.urls.defaults import *
from labzine.articles.models import *
import datetime

issue_dict = {
    # 'queryset': Article.objects.filter(date_modified__lte=datetime.datetime.now()).filter(status__in=['A','B']).order_by('-date_modified'),
    'queryset': Issue.objects.all(),
    'template_object_name': 'issue',
}

article_dict = {
    # 'queryset': Article.objects.filter(date_modified__lte=datetime.datetime.now()).filter(status__in=['A','B']).order_by('-date_modified'),
    'queryset': Article.objects.all(),
    'template_object_name': 'article',
    # "extra_context" : {
    #     "current_issue" : Issue.objects.latest()
    # }
}

article_home_dict = {
    # 'queryset': Article.objects.filter(date_modified__lte=datetime.datetime.now()).filter(status__in=['A','B']).order_by('-date_modified'),
    'queryset': Article.objects.all(),
    'template_object_name': 'article',
}

        
urlpatterns = patterns('',
    # /issues/0_5/
    (r'^(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(issue_dict, slug_field='slug')),
    # /issues/0_5/articles/intro/
    (r'^(?P<slug>[-\w]+)/articles/$', 'django.views.generic.list_detail.object_detail', dict(issue_dict, slug_field='slug', template_name='articles/article_homepage.html')),
    # /issues/0_5/features/
    (r'^(?P<slug>[-\w]+)/features/$', 'django.views.generic.list_detail.object_detail', dict(issue_dict, slug_field='slug', template_name='articles/features_list.html')),
    # (r'^(?P<slug>[-\w]+)/articles/highest_rated$', 'django.views.generic.list_detail.object_detail', dict(highest_rated, slug_field='slug', template_name='articles/highest_rated.html')),
    # /issues/0_5/articles/article-foo/
    # wrapping in view to get the session data
    (r'^([-\w]+)/articles/(?P<slug>[-\w]+)/$', 'labzine.articles.views.article_detail'),
    # (r'^foo/(?P<slug>[-\w]+)/$', 'labzine.articles.views.article_detail2'),
    # (r'^([-\w]+)/articles/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(article_dict, slug_field='slug')),
    # /events/conventions/stumptown_comix
    # (r'^([-\w]+)/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(event_dict, slug_field='slug')),

    # /events/conventions/
    # (r'^(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(category_dict, slug_field='slug')),
    # /events/conventions/stumptown_comix
    # (r'^([-\w]+)/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(event_dict, slug_field='slug')),
)

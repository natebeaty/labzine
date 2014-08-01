from django.conf.urls.defaults import *
from labzine.tagsfield.models import Tag
from labzine.articles.feeds import *
from labzine.blog.feeds import *
from labzine.articles.models import *

from django.contrib import admin
admin.autodiscover()
# from django.contrib.comments.feeds import LatestFreeCommentsFeed
# from django.contrib.comments.models import FreeComment

tag_dict = {
    'queryset': Tag.objects.all(), 
    'template_object_name': 'tag',
}

# comments_info_dict = {
#     'queryset': FreeComment.objects.all(),
#     'paginate_by': 15,
# }

feeds = {
    'articles': ArticlesFeed,
    'blog': BlogFeed,
    # 'comments': LatestFreeCommentsFeed,
}

project_dict = {
    'queryset': Project.objects.all(),
    'template_object_name': 'project',
    "extra_context" : {
        "issue_list" : Issue.objects.all(),
        "current_issue" : Issue.objects.latest()
    }
}

issue_dict = {
    'queryset': Issue.objects.all(),
    'template_object_name': 'issue',
    'template_name': 'articles/project_byissue.html',
    "extra_context" : {
        "issue_list" : Issue.objects.all(),
        "current_issue" : Issue.objects.latest()
    }
}

urlpatterns = patterns('',
    # (r'^fix_people/(?P<start>[\d]+)/(?P<stop>[\d]+)/$', 'labzine.articles.utils.fix_people'),  
    # kludge for /rate/clear/article/4/
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clearcache$', 'labzine.articles.views.clearcache'),
    url(r'^rate/(?P<action>[\w]+)/(?P<item_type>[\w]+)/(?P<item_id>[\d]+)/$', 'labzine.articles.views.rate'),
    url(r'^rate/(?P<action>[\w]+)/(?P<item_type>[\w]+)/(?P<item_id>[\d]+)/(?P<rating>[\d]+)/$', 'labzine.articles.views.rate'),  
    url(r'^toggle_pageflipper/$', 'labzine.articles.views.toggle_pageflipper'),  
    # for article homepage, start pageflipper at 0 -- id=issue_id
    url(r'^pageflip/homepage_(?P<id>\d+)\.xml$', 'labzine.articles.views.pageflip_xml', dict(homepage="true")),
    # for article detail page, start pageflipper at article.start_page+1 -- id=article_id
    url(r'^pageflip/(?P<id>\d+)\.xml$', 'labzine.articles.views.pageflip_xml'),
    url(r'^blog/', include('labzine.blog.urls')),
    url(r'^issues/', include('labzine.articles.urls')),
    # url(r'^contact/$', 'labzine.articles.views.contact_form'),
    url(r'^projects/issue(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(issue_dict, slug_field='slug')),
    # url(r'^([-\w]+)/articles/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(article_dict, slug_field='slug')),
    url(r'^projects/$', 'django.views.generic.list_detail.object_list', project_dict),
    url(r'^browse/$', 'labzine.articles.views.browse'),
    # url(r'^admin/', admin.site.root), # include('django.contrib.admin.urls')),
    # url(r'^comments/$', 'django.views.generic.list_detail.object_list', comments_info_dict),
    # url(r'^comments/', include('django.contrib.comments.urls.comments')),
    url(r'^tag/(?P<slug>[-\w]+)/$','django.views.generic.list_detail.object_detail', dict(tag_dict, slug_field='norm_value')),
    url(r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':'/Users/natebeaty/django/django_projects/labzine/media/'}),
    # url(r'^admin_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':'/Users/natebeaty/django/django_projects/labzine/media/admin_media/'}),
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':'/users/home/natron46/django_projects/labzine/media/'}),
    # url(r'^admin_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':'/users/home/natron46/django_projects/labzine/media/admin_media/'}),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog',{'packages': 'django.conf'}),
    url(r'^(favicon.ico)$', 'django.views.static.serve',{'document_root': '/users/home/natron46/django_projects/labzine/media/'}),
    # url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/issues/0_5/'}),
    url(r'^/?$', 'labzine.articles.views.homepage'),
    url(r'', include('django.contrib.flatpages.urls')),
)

# lab-zine.com/issues/<issue>/articles/<article>/<slug> -- shows single entry
# lab-zine.com/issues/ -- shows most recent entries


# lab-zine.com/issues/0.5/articles/mystery-illustrator/
# lab-zine.com/issues/0.5/people/derek-powazek/
# lab-zine.com/issues/0.5/tags/web/
# lab-zine.com/issues/0.5/ranking/4/

# lab-zine.com/

#lab-zine.com/media/pdf/

# FLATPAGES
# lab-zine.com/about/ 

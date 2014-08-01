from django.contrib.syndication.feeds import Feed
from labzine.blog.models import *
import datetime

class BlogFeed(Feed):
    title = "LAB blog"
    link = "http://lab-zine.com/blog/"
    description = "The latest blog entries from LAB."

    def items(self):
        return Blog.objects.filter(date_added__lte=datetime.datetime.now()).filter(status__exact='A').order_by('-date_added')[:10]

# class BlogCommentsFeed(Feed):
#     title = "LAB blog"
#     link = "http://lab-zine.com/blog/"
#     description = "The latest blog entries from LAB."
# 
#     def items(self):
#         return Blog.objects.filter(date_added__lte=datetime.datetime.now()).filter(status__exact='A').order_by('-date_added')[:10]

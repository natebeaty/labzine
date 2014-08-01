from django.contrib.syndication.feeds import Feed
from labzine.articles.models import Article
import datetime

class ArticlesFeed(Feed):
    title = "LAB articles"
    link = "http://lab-zine.com/"
    description = "The latest articles from LAB."

    def items(self):
        return Article.objects.filter(date_added__lte=datetime.datetime.now()).filter(status__exact='A').order_by('-date_added')[:10]


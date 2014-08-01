from labzine.articles.models import *
from django.http import HttpResponse

def fix_people(request,start,stop):
    """ fixpeople
    
        lab-zine.org/fix_people/1/10/
    """
    from django.db import connection
    cursor = connection.cursor()
    a = Article.objects.all()[int(start):int(stop)]
    s = ""
    for article in a:
        foo = "INSERT INTO articles_article_person(article_id,person_id) VALUES(%s,%s)" % (article.id,article.oldperson)
        s += "%s;\n" % (foo)
        # cursor.execute(foo)
            
    return HttpResponse("<h3>fix people results:</h3><textarea cols='80' rows='40'>%s</textarea>" % (s))

# def get_geocodes(request,start,stop):
#     """ gets geocodes for articles
#     
#         pdxguide.org/get_geocodes/1/10/
#     """
#     from django.db import connection
#     cursor = connection.cursor()
#     a = Article.objects.all()[int(start):int(stop)]
#     s = ""
# 	# p = re.compile(r'(st)\.', re.I)
#     for article in a:
#         if article.address:
#             s += "%s\t%s\t%s\tPortland\tOr\n" % (article.id,article.name,article.address)
#         #     addr = Geocoder(settings.YAHOO_ID,"%s Portland, OR" % article.address)
#         #     if addr.result_count > 0 and isFloat(addr.addresses[0]['Latitude']):
#         #         # article.address = p.sub(r'\1', article.address)
#         #         article.latitude = addr.addresses[0]['Latitude']
#         #         article.longitude = addr.addresses[0]['Longitude']
#         #         s += "<strong>%s added with lat: %s, long: %s (%s)</strong><br />" % (article.name, article.latitude, article.longitude,article.address)
#         #         cursor.execute("UPDATE guide_article SET latitude='%s',longitude='%s',address='%s' WHERE id = '%s'" % (article.latitude,article.longitude,article.address,article.id))
#         #     else:
#         #         s += "%s has found no matches for address: %s<br />" % (article.name, article.address)
#         # else:
#         #     s += "%s has no address<br />" % (article.name)
#             
#     return HttpResponse("<h3>geocode results:</h3><textarea cols='80' rows='40'>%s</textarea>" % (s))
# 
# def fix_slugs(request,start,stop):
#     """ gets slugs for articles
#     
#         pdxguide.org/fix_slugs/1/10/
#     """
#     from pdxguide.guide.models import Article
#     from django.http import HttpResponse
#     from django.template.defaultfilters import slugify
#     from django.db import connection
#     cursor = connection.cursor()
#     a = Article.objects.all()[int(start):int(stop)]
#     s = ""
#     for article in a:
#         if article.name:
#             s += "%s <strong>%s</strong>" % (article.name,article.slug)
#             # article.phone = re.sub(r'\D','',article.phone)
#             article.slug = slugify(article.name)
#             s += "=> <strong>%s</strong>\n" % (article.slug)
#             cursor.execute("UPDATE guide_article SET slug='%s' WHERE id = '%s'" % (article.slug,article.id))
#         else:
#             s += "%s has no name\n" % (article.name)
#         s += '<br />'
#         
#     return HttpResponse("<h3>fix slug results:</h3>%s" % (s))
# 
# def move_essays(request,quadrant_id,start,stop):
#     from pdxguide.guide.models import Article,Essay
#     from django.http import HttpResponse
#     a = Article.objects.filter(quadrant__id__exact=int(quadrant_id))[int(start):int(stop)]
#     s = ""
#     for article in a:
#         s += "Article: %s - %s<hr />" % (article.name,article.author)
#         e = Essay(title=article.name, slug=article.slug, body=article.description, author=article.author, section=article.section, status=article.status)
#         s += "<h3>%s</h3>slug: %s<br />body: %s<br />author: %s<br />section: %s<br />status: %s<br />" % (e.title, e.slug, e.body, e.author, e.section, e.status)
#         e.save()
#         article.delete()
#         s += '<hr />'
#         
#     return HttpResponse("<h3>move essays:</h3>%s" % (s))
# 
# from django.db import models, backend
# 
# class SearchQuerySet(models.query.QuerySet):
#     def __init__(self, model=None, fields=None):
#         super(SearchQuerySet, self).__init__(model)
#         self._search_fields = fields
#         
#     def search(self, query):
#         meta = self.model._meta
#         
#         # Get the table name and column names from the model
#         # in `table_name`.`column_name` style
#         columns = [meta.get_field(name,
#                                   many_to_many=False).column
#             for name in self._search_fields]
#         full_names = ["%s.%s" %
#                 (backend.quote_name(meta.db_table),
#                  backend.quote_name(column))
#             for column in columns]
# 
#         # Create the MATCH...AGAINST expressions        
#         fulltext_columns = ", ".join(full_names)
#         match_expr = ("MATCH(%s) AGAINST (%%s)" %
#                       fulltext_columns)
#         
#         # Add the extra SELECT and WHERE options
#         return self.extra(select={'relevance': match_expr},
#                           where=[match_expr],
#                           params=[query, query])
# 
# 
# class SearchManager(models.Manager):
#     def __init__(self, fields):
#         super(SearchManager, self).__init__()
#         self._search_fields = fields
# 
#     def get_query_set(self):
#         return SearchQuerySet(self.model, self._search_fields)
# 
#     def search(self, query):
#         return self.get_query_set().search(query)
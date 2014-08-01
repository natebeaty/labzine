from django import template
from django.template import Library, Node, TemplateSyntaxError
from django.db.models import get_model
from labzine.articles.models import *
import datetime
     
register = Library()
     
class LatestContentNode(Node):
    """
    {% get_latest weblog.Entry 10 as latest_entries %}
    """
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "fourth argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])
get_latest = register.tag(get_latest)

# class RatingVars(Node):
#     """
#     {% get_rating_vars %}
#     """
#     def render(self, context):
#         context['pageflipper_disabled'] =  request.session.get('pageflipper_disabled',False)
#         context['has_rated'] =  request.session.get('rated_article_%s' % a.id,False)
#         context['rating_average'] = rating_average
#         context['rating_percent'] = rating_percent
#         context[self.varname] = self.model._default_manager.all()[:self.num]
#         return '' 
# def get_rating_vars(parser, token):
#     bits = token.contents.split()
#     if len(bits) != 1:
#         raise TemplateSyntaxError, "get_rating_vars takes no arguments"
#     return RatingVars()
# get_rating_vars = register.tag(get_rating_vars)

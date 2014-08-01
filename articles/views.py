from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django import forms
from labzine.articles.models import *
from labzine import settings
import datetime

EXTENSIONS = {
    'Folder':[''],
    'Image':['jpg','gif','png','tif','tiff'],
    'Video':['mov','wmv','mpeg','mpg','avi'],
    'Document':['pdf','doc','rtf','txt','xls','csv'],
}

class Page:
    def __init__(self, src, preLoad='', pageFunction=''):
        self.src, self.preLoad,self.pageFunction = src,preLoad,pageFunction

# custom query function (from http://www.djangosnippets.org/snippets/207/)
def csql(self,query,qkeys):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # build dict for template:
    fdicts = []
    for row in rows:
        i = 0
        cur_row = {}
        for key in qkeys:
            cur_row[key] = row[i]
            i = i+1
        fdicts.append(cur_row)
    return fdicts

def pageflip_xml(request, id='', homepage=''):
    pages = []
    if homepage:
        issue = Issue.objects.get(pk=id)
        startPage = 1
    else:
        current_article = Article.objects.get(pk=id)
        issue = current_article.issue
        startPage = current_article.page_start+1

    num_pages = issue.num_pages
    a = Article.objects.all()

    for i in range(num_pages):
        if i == startPage or i == startPage+1:
            pre_load = 'true';
        else:
            pre_load = '';
        pages.append(Page("http://www.lab-zine.com/media/pageflip/pages/issue%s/issue%s-%02d.jpg" % (issue.slug,issue.slug,i),pre_load))
    
    # for article in a:
    #     ps = article.page_start
    #     pages[ps].pageFunction = "getURL,'http://www.lab-zine.com/issues/%s/articles/%s/'" % (article.issue.slug,article.slug)
        
    return render_to_response('pages.xml', {'pages': pages, 'startPage': startPage})

#     --------------
#     CONTACT FORM
#     --------------

# class ContactManipulator(forms.Manipulator):
#     def __init__(self):
#         self.fields = (
#             forms.EmailField(field_name="from", length=30, is_required=True),
#             forms.TextField(field_name="name", length=30, is_required=True),
#             forms.TextField(field_name="subject", length=30, maxlength=200, is_required=False),
#             forms.LargeTextField(field_name="message", is_required=True),
#             # forms.FileField('/home/natebeaty/django/django_projects/labzine/media/uploads/', is_required=False),
#             forms.FileUploadField(field_name="fileUpload", is_required=False)
#         )

# def contact_form(request):
#     from django.core.mail import send_mail, BadHeaderError,mail_managers 
#     import os
#     # max upload size in bytes
#     MAX_UPLOAD_SIZE = "2000000"
#     #upload path
#     path =  settings.MEDIA_ROOT + 'uploads/'

#     manipulator = ContactManipulator()
#     if request.POST:
#         new_data = request.POST.copy()
#         errors = manipulator.get_validation_errors(new_data)
#         if not errors:
#             if request.FILES:
#                 for file in request.FILES.getlist('fileUpload'):
#                     filename = file['filename'].replace(' ','_')
#                     content = file['content']
                
#                     thispath = path + filename
#                     f = open(thispath, 'wb')
#                     f.write(content)
#                     os.chmod(thispath, 0664)
#                     f.close()
                
#                     new_data['message'] = new_data['message'] + "\n\nFile uploaded: http://%s/media/uploads/%s" % (settings.SITE_URL,filename)
                    
#             manipulator.do_html2python(new_data)
#             to_email = ["natebeaty@gmail.com","josepherobertson@gmail.com"]
#             new_data['message'] = new_data['message'] + "\n\nName: %s" % (new_data['name'])
#             if not new_data['subject']:
#                 new_data['subject'] = 'LAB contact';
#             try:
#                 send_mail(new_data['subject'], new_data['message'], new_data['from'], to_email, fail_silently=False)
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#             return HttpResponseRedirect('/contact/thanks/')
#     else:
#         errors = {};
#         new_data = {};
#         # if request.GET:
#         #     new_data['to'] = request.GET['to']
#         # else:
#         #     new_data['to'] = 'editor'
#     form = forms.FormWrapper(manipulator, new_data, errors)
#     return render_to_response('contact_form.html', {'form': form},
#                                context_instance=RequestContext(request))

#     -----------------------------
#     TOGGLE PAGEFLIPPER W/ COOKIE
#     -----------------------------

def toggle_pageflipper(request):
    if request.session.get('pageflipper_disabled', False):
        request.session['pageflipper_disabled'] = False
    else:
        request.session['pageflipper_disabled'] = True

    # RETURN USER TO PAGE IF THERE IS A REFERER, ELSE HOMEPAGE
    if 'HTTP_REFERER' in request.META:
        originURL = request.META['HTTP_REFERER']
    else:
        originURL = '/'
    return HttpResponseRedirect(originURL)
    # return HttpResponse('pageflipper: %s' % request.session['pageflipper_disabled'])

#     ---------------------
#     ARTICLE DETAIL PAGE  
#     generic view wrapper
#     w/ request.session.pageflipper_disabled
#     ---------------------

def homepage(request):
    try: 
        current_issue = Issue.objects.get(featured=True)
    except:
        current_issue = Issue.objects.filter(active=True).reverse()[0]
    return render_to_response("articles/issue_detail.html", {'issue': current_issue},
                               context_instance=RequestContext(request))

def browse(request):
    from django.views.generic.list_detail import object_list
    from labzine.tagsfield.models import Tag
    import logging
    
    qkeys = ['tag_count','value','norm_value']
    # query = "SELECT COUNT(t.id) as tag_count,t.value,t.norm_value FROM tags_tag t LEFT JOIN blog_blog_tags bt ON (bt.tag_id = t.id) LEFT JOIN articles_article_tags at ON (at.tag_id=t.id) GROUP BY t.id" 
    # just article tags: SELECT COUNT(t.id) as tag_count,t.value,t.norm_value,at.id FROM tags_tag t LEFT JOIN articles_article_tags at ON (at.tag_id=t.id) where at.id is not null GROUP BY t.id 
    query = "SELECT COUNT(t.id) as tag_count,t.value,t.norm_value FROM articles_article_tags at LEFT JOIN tagsfield_tag t ON (at.tag_id=t.id) GROUP BY t.id" 
    tag_cloud = csql(request,query,qkeys)

    for i in range(len(tag_cloud)):
        tag_cloud[i]['pop'] = 'meh'
        if tag_cloud[i]['tag_count'] > 2:
            tag_cloud[i]['pop'] = 'popular'
        if tag_cloud[i]['tag_count'] > 5:
            tag_cloud[i]['pop'] = 'mega-popular'
        if tag_cloud[i]['tag_count'] > 10:
            tag_cloud[i]['pop'] = 'holycrap-popular'

    # featured = Feature.objects.all()[:6] # 6 latest
    featured = Feature.objects.order_by('?')[:6] # randomize
    colors = Article.objects.all().order_by('?')[:60] # filter colors here? meh
    issues = Issue.objects.filter(active=True)
    # favorites = Article.objects.filter(num_ratings__gte=10).order_by('rating_total')[:6]
    favorites = Article.objects.filter(num_ratings__gte=10).order_by('?')[:6]

    # todo: fix favorites query as below:
    # SELECT id,(rating_total / num_ratings) as avg FROM `articles_article` order by avg
    # qkeys = ['tag_count','value','norm_value']
    # query = "SELECT COUNT(t.id) as tag_count,t.value,t.norm_value FROM tags_tag t LEFT JOIN blog_blog_tags bt ON (bt.tag_id = t.id) LEFT JOIN articles_article_tags at ON (at.tag_id=t.id) GROUP BY t.id" 
    # tag_cloud = csql(request,query,qkeys)
    # logging.debug(featured)

    return render_to_response("articles/browse.html", { 'favorites': favorites, 'featured': featured, 'colors': colors, 'issues': issues, 'tag_cloud': tag_cloud },
                               context_instance=RequestContext(request))

def article_detail(request, slug):
    from django.views.generic import list_detail

    article = Article.objects.get(slug=slug)
    if article.rating_total > 0:
        rating_average = '%.1f' % float(float(article.rating_total) / float(article.num_ratings))
        rating_percent =  int(float(article.rating_total) / float(article.num_ratings)*10)
    else:
        rating_average = rating_percent = 0
    
    # set test cookie    
    request.session.set_test_cookie()
    return list_detail.object_detail(
        request,
        slug_field = 'slug',
        queryset = Article.objects.all(),
        template_object_name = 'article',
        template_name = 'articles/article_detail.html',
        slug = slug,
        extra_context = {
            'current_issue' : Issue.objects.get(featured='1'),
            'pageflipper_disabled' : request.session.get('pageflipper_disabled',False),
            'has_rated' : request.session.get('rated_article_%s' % article.id,False),
            'rating_average': "%s" % rating_average,
            'rating_percent': "%s" % rating_percent,
        }
    )

#     ------------------
#     RATING AJAX VIEW
#     ------------------

def rate(request,action,item_type,item_id,rating=''):
    if 'HTTP_REFERER' in request.META:
        originURL = request.META['HTTP_REFERER']
    else:
        originURL = '/'

    article = Article.objects.get(pk=item_id)
    if request.session.test_cookie_worked():
        if action == 'add':
            # make sure user hasn't voted for this article yet
            if 'rated_%s_%s' % (item_type,item_id) in request.session:
                r = article.ratings.get(session_key=request.session.session_key)
                article.rating_total = int(article.rating_total) - int(r.rating) + int(rating)
                r.rating = int(rating)
                r.save()
                article.save()
                # article.update_ratings()
                message='new rating saved!';
            else:
            
                # Update rating totals
                article.rating_total = int(article.rating_total) + int(rating) 
                article.num_ratings = int(article.num_ratings) + 1
                article.save()
        
                # Post rating to db and add relation to article
                r = Rating(session_key=request.session.session_key,rating=rating)
                r.save()
                article.ratings.add(r)
        
                # mark as voted
                request.session['rated_%s_%s' % (item_type,item_id)] = True

                message = 'rating saved ok!'

        elif action == 'clear':
            r = article.ratings.get(session_key=request.session.session_key)
            # Update rating totals
            article.rating_total = int(article.rating_total) - int(r.rating) 
            article.num_ratings = int(article.num_ratings) - 1
            article.save()
            # clear rating
            r.delete()
            # clear voted cookie
            del request.session['rated_%s_%s' % (item_type,item_id)]
            message = 'rating cleared ok!'
    else:
        message = 'cookies not enabled!'

    if article.rating_total > 0:
        rating_average = round(float(float(article.rating_total) / float(article.num_ratings)),1)
        rating_percent = float(float(article.rating_total) / float(article.num_ratings) * 10)
    else:
        rating_average = rating_percent = 0

    extra_context = {
      'current_issue' : article.issue,
      # 'current_issue' : Issue.objects.get(featured='1'),
      'pageflipper_disabled' : request.session.get('pageflipper_disabled',False),
      'has_rated' : request.session.get('rated_%s_%s' % (item_type,item_id),False),
      'rating_average': "%s" % rating_average,
      'rating_percent': "%s" % rating_percent,
      'article': article,
      'message': message,
    }
    if 'ajaxed' in request.GET:
        return render_to_response('articles/rating.html', extra_context)
    else:
        return HttpResponseRedirect(originURL)
    # return HttpResponse(jsonList)

def clearcache(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE cache")
    return HttpResponseRedirect('/')

from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime
from labzine.middleware import threadlocals
# from verdjnlib.fields import ImageField, PhotoField, CROP, FIT
from labzine.tagsfield.models import Tag
from labzine.tagsfield import fields

from labzine import settings
import re

STATUS_CHOICES = (
	('A','Active'),
	('N','Not Active'),
    )
RATING_CHOICES = (
	('1','Try again'),
	('2','Not so good'),
	('3','Good'),
	('4','Great!'),
	('5','Holy Crap Batman'),
    )

class Link(models.Model):
    name = models.CharField(blank=True, max_length=250)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, editable=False, auto_now=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ('name',)
        get_latest_by = 'date_added'
    class Admin:
        pass
        ordering = ["name"]
        date_hierarchy = 'date_added'
        list_display = ('name', 'description', 'url')
        search_fields = ('name', 'url', 'description')
        list_filter = ('date_added',)

class Slogan(models.Model):
    slogan = models.TextField()
    def __unicode__(self):
        return self.slogan
    class Admin:
        pass

class Issue(models.Model):
    slug = models.SlugField( 'Slug', help_text='Automatically built from the name.', )
    name = models.CharField(max_length=200)
    num_pages = models.IntegerField(blank=True)
    description = models.TextField(null=True, blank=True)
    printpdf = models.CharField(max_length=100, blank=True, null=True, help_text='Upload to media/pdf/issues/ -- for this field type in "pdf/issues/filename.pdf" (omit media/)')
    # printpdf = models.FileField(upload_to='pdf/issues', blank=True, null=True)
    printpdf_size = models.CharField(max_length=200, blank=True, null=True)
    # webpdf = models.CharField(max_length=100, blank=True, null=True, help_text='Upload to media/pdf/issues/ -- for this field type in "pdf/issues/filename.pdf" (omit media/)')
    webpdf = models.FileField(upload_to='pdf/issues', blank=True, null=True)
    webpdf_size = models.CharField(max_length=200, blank=True, null=True)
    print_version_link = models.URLField(null=True, blank=True, verify_exists=False)
    image = models.ImageField(upload_to='images/issues', blank=True, null=True)
    # image = PhotoField(upload_to='images/issues', width=300, height=500, blank=True, null=True)
    # thumb = PhotoField(upload_to='images/issues', width=75, height=75, blank=True, null=True)
    issue_logo = models.ImageField(upload_to='images/issues', blank=True, null=True)
    hex_color = models.CharField(max_length=6,blank=True)
    date_added = models.DateTimeField(blank=True, auto_now_add=True)
    featured = models.BooleanField(help_text='Note that you must manually deselect previously featured issues.')
    active = models.BooleanField(help_text='Whether or not to show in the navbar Issues >> drop down.')
    def __unicode__(self):
        return self.name
    class Admin:
        pass
    class Meta:
        get_latest_by = 'date_added'
        ordering = ('name',)
    def get_absolute_url(self):
        return "/issues/%s/" % (self.slug)

class Person(models.Model):
    slug = models.SlugField( 'Slug', help_text='Automatically built from the name.')
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, help_text='Use this field if only a single name.',)
    url = models.CharField(blank=True, null=True,max_length=250)
    url2 = models.CharField(blank=True, null=True,max_length=250)
    url3 = models.CharField(blank=True, null=True,max_length=250)
    url4 = models.CharField(blank=True, null=True,max_length=250)
    links = models.ManyToManyField(Link,blank=True,null=True, verbose_name="Links related to person")
    description = models.TextField(null=True, blank=True)
    # thumb = PhotoField(upload_to='images/person', width=75, height=75, blank=True, null=True)
    def __unicode__(self):
        return "%s %s" % (self.first_name,self.last_name)
    class Admin:
        pass
    class Meta:
        verbose_name_plural = 'people'
        ordering = ('last_name','first_name',)
    def get_absolute_url(self):
        return "/people/%s/" % (self.slug)
        
class Project(models.Model):
    slug = models.SlugField(
        'Slug',
        help_text='Used for linking -- this must be unique and contain no spaces.',
        blank=True,
        unique=True,
    )
    issue = models.ForeignKey(Issue)
    tags = fields.TagsField(Tag,blank=True, null=True)
    title = models.CharField(max_length=200)
    project_url = models.CharField(blank=True, null=True,max_length=250)
    description = models.TextField(blank=True, null=True)
    image_large = models.CharField(max_length=250, blank=True, null=True)
    image_large_url = models.CharField(blank=True, null=True,max_length=250)
    image_small1 = models.CharField(max_length=250, blank=True, null=True)
    image_small1_url = models.CharField(blank=True, null=True,max_length=250)
    image_small2 = models.CharField(max_length=250, blank=True, null=True)
    image_small2_url = models.CharField(blank=True, null=True,max_length=250)
    status = models.CharField(max_length=5,choices=STATUS_CHOICES,default='A')
    date_added = models.DateTimeField(blank=True, auto_now_add=True)
    date_modified = models.DateTimeField(editable=False,blank=True, auto_now=True)

    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return "/projects/issue%s/" % (self.issue.slug)
    def is_active(self):
        return self.status == 'A'
    class Admin:
        pass
        ordering = ["-date_modified"]
        date_hierarchy = 'date_modified'
        list_display = ('project_num', 'title', 'issue')
        search_fields = ('title', 'body')
        list_filter = ('date_modified', 'status')
        js = ('js/tags.js',)
    def project_num(self):
        return 'Project %02d' % (self.id)
    class Meta:
        ordering = ('date_added','title')
        get_latest_by = 'date_added'

class Rating(models.Model):
    session_key = models.CharField(max_length=200)
    rating = models.SmallIntegerField(max_length=1, choices=RATING_CHOICES)
    post_date = models.DateTimeField(auto_now=True, editable=False)
    
class Article(models.Model):
    slug = models.SlugField(
        'Slug',
        help_text='Used for linking -- this must be unique and contain no spaces.',
        blank=True,
        unique=True,
    )
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Person,blank=True,null=True, verbose_name="Author(s) of article", related_name='author_articles')
    person = models.ManyToManyField(Person,blank=True,null=True, verbose_name="People related to article", related_name='person_articles')
    issue = models.ForeignKey(Issue)
    links = models.ManyToManyField(Link,blank=True,null=True, verbose_name="Links related to article")
    ratings = models.ManyToManyField(Rating,blank=True,null=True,editable=False)
    num_ratings = models.IntegerField(editable=False,blank=True,default=0)
    rating_total = models.IntegerField(editable=False,blank=True,default=0)
    display_page_number = models.IntegerField(blank=True,null=True)
    page_start = models.IntegerField(blank=True,null=True)
    page_end = models.IntegerField(blank=True,null=True)
    image_left = models.FileField(upload_to='images/articles', blank=True, null=True)
    image_right = models.FileField(upload_to='images/articles', blank=True, null=True)
    hex_color = models.CharField(max_length=6,blank=True)
    printpdf = models.FileField(upload_to='pdf/articles/', blank=True, null=True)
    webpdf = models.FileField(upload_to='pdf/articles/', blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, auto_now_add=True)
    date_modified = models.DateTimeField(editable=False,blank=True, auto_now=True)
    status = models.CharField(max_length=5,choices=STATUS_CHOICES,default='A')
    tags = fields.TagsField(Tag, blank=True, null=True)


    def __unicode__(self):
        return self.title.encode('utf-8')
    def is_active(self):
        return self.status == 'A'
    def get_absolute_url(self):
        return "/issues/%s/articles/%s/" % (self.issue.slug, self.slug)
    def art_people(self):
        pset = self.person.all()
        r = ''
        for p in pset:
            r += "%s %s, " % (p.first_name,p.last_name)
        return r[:-2]
    def art_authors(self):
        pset = self.author.all()
        r = ''
        for p in pset:
            r += "%s %s, " % (p.first_name,p.last_name)
        return r[:-2]
    # def update_ratings(self):
    #     if self.ratings:
    #         rating_list = self.ratings.all()
    #         rating_total = 0
    #         for r in rating_list:
    #             rating_total += r.rating
    #         self.num_ratings = len(rating_list)
    #     else:
    #         self.num_ratings, self.rating_total = 0, 0
    #     self.save()
    class Admin:
        pass
        ordering = ["-issue", "page_start"]
        date_hierarchy = 'date_modified'
        list_display = ('title', 'issue', 'art_people','art_authors','display_page_number','page_start','page_end', 'status')
        search_fields = ('title','author','person')
        list_filter = ('date_modified', 'status', 'issue')
        js = ('js/tags.js',)
    class Meta:
        ordering = ('page_start','date_added','title')
        get_latest_by = '-date_added'

class Feature(models.Model):
    issue = models.ForeignKey(Issue)
    article = models.ForeignKey(Article)
    text = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, auto_now_add=True)
    # image = PhotoField(upload_to='images/features', width=100, height=100, blank=True, null=True, mode=CROP, quality=85)
    image = models.ImageField(upload_to='images/features', blank=True, null=True)
    order_code = models.CharField(max_length=6,blank=True,null=True)

    def __unicode__(self):
        return self.article.title
    class Admin:
        pass
    class Meta:
        ordering = ('order_code',)
        get_latest_by = 'date_added'

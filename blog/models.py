from django.db import models
from datetime import datetime
# from verdjnlib.fields import *
from labzine.tagsfield.models import Tag
from labzine.tagsfield import fields

from labzine import settings
import re

STATUS_CHOICES = (
	('A','Active'),
	('N','Not Active'),
    )

class Category(models.Model):
    slug = models.SlugField( 'Slug', help_text='Automatically built from the name.', )
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return self.name
    class Admin:
        pass
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('name',)
    def get_absolute_url(self):
        return "/illos/%s/" % (self.slug)

class Blog(models.Model):
    slug = models.SlugField(
        'Slug',
        help_text='Used for linking -- this must be unique and contain no spaces.',
        blank=True,
        unique=True,
    )
    category = models.ForeignKey(Category)
    tags = fields.TagsField(Tag,blank=True, null=True)
    title = models.CharField(max_length=200)
    excerpt = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='images/blog', 
        # width=150, height=200, mode=FIT, quality=85, 
        null=True, blank=True,
        # help_text='Optional image, sized to fit 150px x 200px.',
        )
    status = models.CharField(max_length=5,choices=STATUS_CHOICES,default='A')
    date_added = models.DateTimeField(blank=True, auto_now_add=True)
    date_modified = models.DateTimeField(editable=False,blank=True, auto_now=True)

    def __unicode__(self):
        return self.title.encode('utf-8')
    def is_active(self):
        return self.status == 'A'
    def get_absolute_url(self):
        return "/blog/%s/%s/" % (self.date_added.strftime("%Y/%b/%d").lower(), self.slug)
    class Admin:
        pass
        ordering = ["-date_modified"]
        date_hierarchy = 'date_modified'
        list_display = ('title', 'status')
        search_fields = ('title', 'body')
        list_filter = ('date_modified', 'status')
        js = ('js/tags.js',)
    class Meta:
        ordering = ('date_added','title')
        get_latest_by = 'date_added'

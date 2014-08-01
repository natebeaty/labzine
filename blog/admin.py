from labzine.blog.models import Category, Blog
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class CategoryOptions(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class BlogOptions(admin.ModelAdmin):
    ordering = ["-date_modified"]
    date_hierarchy = 'date_modified'
    list_display = ('title', 'status')
    search_fieldsets = ('title', 'body')
    list_filter = ('date_modified', 'status')
    js = ('js/tags.js',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryOptions)
admin.site.register(Blog, BlogOptions)

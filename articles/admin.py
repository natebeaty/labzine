from labzine.articles.models import Link, Slogan, Issue, Person, Project, Article, Feature
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class ProjectOptions(admin.ModelAdmin):
    ordering = ["-date_modified"]
    date_hierarchy = 'date_modified'
    list_display = ('project_num', 'title', 'issue')
    search_fieldsets = ('title', 'body')
    list_filter = ('date_modified', 'status')
    js = ('js/tags.js',)
    prepopulated_fields = {'slug': ('title',)}

class PersonOptions(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name','last_name',)}
    filter_horizontal = ('links',)

class LinkOptions(admin.ModelAdmin):
    ordering = ["name"]
    date_hierarchy = 'date_added'
    list_display = ('name', 'description', 'url')
    search_fieldsets = ('name', 'url', 'description')
    list_filter = ('date_added',)

class ArticleOptions(admin.ModelAdmin):
    ordering = ["-issue", "page_start"]
    date_hierarchy = 'date_modified'
    list_display = ('title', 'issue', 'art_people','art_authors','display_page_number','page_start','page_end', 'status')
    search_fieldsets = ('title','author','person')
    list_filter = ('date_modified', 'status', 'issue')
    js = ('js/tags.js',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('author', 'person', 'links')

class IssueOptions(admin.ModelAdmin):
    ordering = ["name"]
    date_hierarchy = 'date_added'
    list_display = ('name', 'webpdf', 'featured', 'active')
    search_fields = ('name', 'description')
    list_filter = ('active', 'featured')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Slogan)
admin.site.register(Feature)
admin.site.register(Project, ProjectOptions)
admin.site.register(Person, PersonOptions)
admin.site.register(Link, LinkOptions)
admin.site.register(Article, ArticleOptions)
admin.site.register(Issue, IssueOptions)


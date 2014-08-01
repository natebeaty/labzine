# TagsField for Django
  

## What is it
  
TagsField -- is a small app for [Django](http://www.djangoproject.com/),
that implements tagging for arbitrary objects in your applications with
a form control for editing tags.

The application contains:

- Tag model representing tag's value (a word) without any additional fields.
  It can be extended as you like.
- New field class TagsField which is basically a standard ManyToManyField
  extended to support its own form control.
- Form control for editing tags with an autocomplete 
- Autocomplete is case insensitive and also ignores insignificant differences
  in spelling (ignores punctuation, whitespace and the word "the")

Tags creation is entirely 'user-managed' meaning that when a user adds a tag
that does not exist it is created automatically.


## How to use it

Download and place the app's directory somewhere into your project directory,
add it to INSTALLED_APPS in your settings. Also make sure that you have enabled
`django.template.loaders.app_directories.load_template_source` in the 
TEMPLATE_LOADERS setting. This is needed for TagsField to find the template for the
form control.

Add tags to your model:
  
    from myproject.tags.models import Tag
    from myproject.tags import fields
    
    class Article(models.Model):
      ...
      tags = fields.TagsField(Tag)
  
Now you can use the field "tags" the same as the default ManyToManyField. The
only difference is that in forms made with automatic manipulators (including
those in generic views) tags will be displayed as a set of autocomplete 
controls (see. included demo.html)

You can include this form field in custom manipulators like this:

    from django.forms import Manipulator
    from myproject.tags import fields
    
    class MyManipulator(Manipulator):
      def __init__(self):
        self.fields = [
          ...
          fields.TagsFormField('tags'),
        ]

Tags are usually stored in the library's built-in Tag model. They are 
used for auto-completion in forms. If you use your own model instead of
the default one you should teach a manipulator field to look there:

    self.fields = [
      ...
      fields.TagsFormField('tags', model=some.other.TagModel),
    ]


## Settings
  
In most cases it's enough to set two settings:

`JS_URL`
: URL to the location where the file "tags.js" is located. You can move it 
  to your own script directory or leave it in its original location.
  
`STYLE_URL`
: URL to the location with the file "tags.css" and graphics.

If these two settings are not set then by default these locations will be 
`/media/js/` and `/media/css/`. These are common locations for Django projects.

There's another optional setting:

`TAGS_URL`
: URL to the "tag's page" on your site (if you plan to have one). Usually 
  it shows a list of objects that are linked to a certain tag. The setting
  should be in the form of 'http://domain/path/%s/' where %s is replaced with
  tag's value.
  If not set then tags are displayed without links at all.
  
## Usage in Django admin
  
The field will be automatically displayed in admin but for it to actually 
work you should include tag's javascript to the admin's javascript list:

    class MyModel(models.Model):
      ...
      
      class Admin:
        js = (
          'js/tags.js',
        )

Since the admin uses relative URLs the file "tags.js" should be copied into the
admin's media directory.

In the same fashion the tag's CSS and graphics should also be copied to the [admin's
CSS](http://www.djangoproject.com/documentation/admin_css/).


## About

Version: 1.8
URL:    http://softwaremaniacs.org/soft/tags/en/
Author:  Ivan Sagalaev (Maniac@SoftwareManiacs.Org)
from django.db import models
from django.db.models.loading import get_app
from django.conf import settings
from labzine.tags.utils import normalize_title

class Tag(models.Model):
  value = models.CharField(max_length=50)
  norm_value = models.CharField(max_length=50, editable=False)
  
  class Meta:
    ordering=('norm_value','value')
  
  def __str__(self):
    return self.value
    
  def save(self):
    tags = get_app('tags')
    self.norm_value = normalize_title(self.value)
    super(Tag, self).save()
    
  def get_absolute_url(self):
    if not getattr(settings, 'TAGS_URL', ''):
      return ''
    from urllib import quote
    try:
      return settings.TAGS_URL % quote(self.value)
    except TypeError:
      return settings.TAGS_URL + quote(self.value)

  class Admin:
    pass

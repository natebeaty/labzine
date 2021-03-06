import os
from django.db import models
from django import forms
from django.utils.functional import curry
from verdjnlib.fields import DeleteCheckbox


class FileField(models.FileField):

    def get_internal_type(self):
        return 'FileField'

    def get_manipulator_field_objs(self):
        # Only show DeleteCheckbox if null=True
        if self.null:
            return [forms.FileUploadField, forms.HiddenField, DeleteCheckbox]
        else:
            return [forms.FileUploadField, forms.HiddenField]

    def get_manipulator_field_names(self, name_prefix):
        # Only show DeleteCheckbox if null=True
        if self.null:
            return [name_prefix + self.name + '_file', name_prefix + self.name, name_prefix + self.name + '_delete']
        else:
            return [name_prefix + self.name + '_file', name_prefix + self.name]

    def save_file(self, new_data, new_object, original_object, change, rel, save=True):
        field_names = self.get_manipulator_field_names('')
        # Delete only if DeleteCheckbox is present and checked
        if len(field_names) > 2 and new_data.get(field_names[2], False):
            file_name = getattr(new_object, 'get_%s_filename' % self.name)()
            # If file exists, delete it
            if file_name and os.path.exists(file_name):
                os.remove(file_name)
            setattr(new_object, self.name, None)
            new_object.save()
        else:
            super(FileField, self).save_file(new_data, new_object, original_object, change, rel, save)


# The following code is identical to the ImageField class in
# django/db/models/fields/.__init__.py except for get_manipulator_field_objs()
# and the fact that it inherits from verdjnlib.FileField (above)

class ImageField(FileField):
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        self.width_field, self.height_field = width_field, height_field
        FileField.__init__(self, verbose_name, name, **kwargs)

    def get_manipulator_field_objs(self):
        if self.null:
            return [forms.ImageUploadField, forms.HiddenField, DeleteCheckbox]
        else:
            return [forms.ImageUploadField, forms.HiddenField]

    def contribute_to_class(self, cls, name):
        super(ImageField, self).contribute_to_class(cls, name)
        # Add get_BLAH_width and get_BLAH_height methods, but only if the
        # image field doesn't have width and height cache fields.
        if not self.width_field:
            setattr(cls, 'get_%s_width' % self.name, curry(cls._get_FIELD_width, field=self))
        if not self.height_field:
            setattr(cls, 'get_%s_height' % self.name, curry(cls._get_FIELD_height, field=self))

    def save_file(self, new_data, new_object, original_object, change, rel, save=True):
        FileField.save_file(self, new_data, new_object, original_object, change, rel, save)
        # If the image has height and/or width field(s) and they haven't
        # changed, set the width and/or height field(s) back to their original
        # values.
        if change and (self.width_field or self.height_field):
            if self.width_field:
                setattr(new_object, self.width_field, getattr(original_object, self.width_field))
            if self.height_field:
                setattr(new_object, self.height_field, getattr(original_object, self.height_field))
            new_object.save()


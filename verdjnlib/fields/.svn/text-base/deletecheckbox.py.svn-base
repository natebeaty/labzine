from django.forms import CheckboxField
from django.utils.translation import gettext


class DeleteCheckbox(CheckboxField):

    def __init__(self, field_name, checked_by_default=False, validator_list=None, is_required=False):
        super(DeleteCheckbox, self).__init__(field_name, checked_by_default, validator_list)

    def render(self, data):
        checked_html = ''
        if data or (data is '' and self.checked_by_default):
            checked_html = ' checked="checked"'
        label = gettext('Delete')
        return ' %s <input type="checkbox" id="%s" class="v%s" name="%s"%s value="on" />' % \
            (label, self.get_id(), self.__class__.__name__,
            self.field_name, checked_html)

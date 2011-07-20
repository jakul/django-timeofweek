import re

from django.db.models import CharField
from django.utils.translation import ugettext_lazy
from timeofweek import form_fields

class TimeOfWeekField(CharField):
    description = ugettext_lazy("Time of Week field")
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 4000)
        super(TimeOfWeekField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {
            'form_class': form_fields.TimeOfWeekField,
            'max_length': self.max_length
        }
        defaults.update(kwargs)
        return super(TimeOfWeekField, self).formfield(**defaults)

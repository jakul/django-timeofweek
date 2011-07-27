import re

from django.db.models import CharField
from django.utils.translation import ugettext_lazy
from timeofweek import form_fields
from timeofweek.util import TimeOfWeek

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
    
    def to_python(self, value):
        if not value:
            return None
        return TimeOfWeek(value)
    
    def get_db_prep_value(self, value):
        return str(value)

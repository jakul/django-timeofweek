from django.forms.fields import CharField
from timeofweek.util import TimeOfWeek, TimeOfWeekException
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
class TimeOfWeekField(CharField):
    def __init__(self, *args, **kwargs):
        self.default_error_messages['invalid_time_of_week'] = _(
            u'Invalid time of week'
        )
        super(TimeOfWeekField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """
        Validates that int() can be called on the input. Returns the result
        of int(). Returns None for empty values.
        """
        value = super(CharField, self).to_python(value)
        
        try:
            # ensure this is a valid TimeOfWeek string
            TimeOfWeek(value)
        except TimeOfWeekException, ex:    
            raise ValidationError(self.error_messages['invalid_time_of_week'])
        
        return value
     
    
from django.forms.fields import CharField
from timeofweek.util import TimeOfWeek
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from timeofweek.exceptions import TimeOfWeekException

class TimeOfWeekField(CharField):

    def to_python(self, value):
        """
        Validates that int() can be called on the input. Returns the result
        of int(). Returns None for empty values.
        """
        value = super(CharField, self).to_python(value)
        
        try:
            # ensure this is a valid TimeOfWeek string
            tow = TimeOfWeek(value)
        except TimeOfWeekException, ex: 
            raise ValidationError(ex.msg)

        return str(tow)
     
    
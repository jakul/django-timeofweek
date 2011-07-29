from django.forms.fields import CharField
from timeofweek.util import TimeOfWeek
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from timeofweek.exceptions import TimeOfWeekException
from django.forms import widgets

class TimeOfWeekField(CharField):
    
    def __init__(self, *args, **kwargs):
        super(TimeOfWeekField, self).__init__(*args, **kwargs)
        # Do this here, 
        self.widget = widgets.Textarea()
        
    def to_python(self, value):
        value = super(CharField, self).to_python(value)
        
        try:
            # ensure this is a valid TimeOfWeek string
            tow = TimeOfWeek(value)
        except TimeOfWeekException, ex: 
            raise ValidationError(ex.msg)

        return tow.to_json()
     
    
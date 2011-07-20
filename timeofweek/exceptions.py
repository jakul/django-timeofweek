class TimeOfWeekException(Exception):
    exception_type = None
    
    @property
    def msg(self):
        if self.exception_type is None:
            return 'TimeOfWeekException: ' + str(self.args)
        else:
            message = '%(value)s is not a valid %(type)s' % {
                'value': self.args[0], 'type':self.exception_type
            }
            
            if len(self.args)> 1:
                for arg in self.args[1:]:
                    message += '. %s' % str(arg)
            return message
        

class InvalidTimeOfWeekException(TimeOfWeekException):
    exception_type = 'day/time'  

class InvalidDayException(TimeOfWeekException):
    exception_type = 'day'

class InvalidTimeException(TimeOfWeekException):
    exception_type = 'time'

class InvalidPeriodException(TimeOfWeekException):
    exception_type = 'time period'

class InvalidTimePeriodException(TimeOfWeekException):
    exception_type = 'time period'
      
#
#class InvalidTimeOfWeekException(TimeOfWeekException):
#    
#    @property
#    def msg(self):
#        return '%d is not a valid day/time' % (self.args[0])    
#
#
#class InvalidDayException(TimeOfWeekException):
#    
#    @property
#    def msg(self):
#        return '%d is not a valid day' % (self.args[0])
#
#class InvalidTimeException(TimeOfWeekException):
#    
#    @property
#    def msg(self):
#        return '%d is not a valid time' % (self.args[0])
#
#
#class InvalidPeriodException(TimeOfWeekException):
#    
#    @property
#    def msg(self):
#        return '%s is not a valid time period' % (str(self.args[0]))
#
#class InvalidTimePeriodException(TimeOfWeekException):
#
#    @property
#    def msg(self):
#        return '%s is not a valid time period' % (str(self.args[0]))
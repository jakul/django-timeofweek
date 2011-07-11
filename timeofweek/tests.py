from django.test import TestCase
from timeofweek.util import TimeOfWeek


class TimeOfWeekTest(TestCase):
    
    def setUp(self):
        self.day_names = (
          'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN', 'HOL'
        )
        self.times = ('0000', '0920', '1200', '1545', '2359')

        self.invalid_days = ('M', 'T', 'monday', 'ananan')
        self.invalid_times = ('12345', '', '1', '123', '12', None, '-1')
        
    def test_basic(self):
        #this represents all times in the week
        tow = TimeOfWeek()
        
        for day in self.day_names:
            for time in self.times:
                self.assertTrue(day + time in tow)
        

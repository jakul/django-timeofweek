from django.test import TestCase
from timeofweek.util import TimeOfWeek, InvalidTimeOfWeekException,\
    InvalidDayException, InvalidTimeException, InvalidPeriodException


class TimeOfWeekTest(TestCase):
    
    def setUp(self):
        self.day_names = (
          'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN', 'HOL'
        )
        self.times = ('0000', '0920', '1200', '1545', '2359')

        self.invalid_days = ('M', 'T', 'monday', 'ananan')
        self.invalid_days2 = ('ABC', 'MOO')
        self.invalid_times = ('12345', '', '1', '123', '12', '-1', '1.2')
        self.invalid_times2 = ('3000', '9999')
        
        
        
    def test_tow(self):
        """
        Test the parsing of dates/time from a number of strings
        Test the parsing of periods
        Test the storage of periods
        """
        tow = TimeOfWeek()
        
        self.assertFalse(None in tow)
        
        for day in self.day_names:
            for time in self.times:
                self.assertTrue(day + time in tow)
            for time in self.invalid_times:
                self.assertRaises(
                    InvalidTimeOfWeekException, tow.__contains__, day + time
                )          
            for time in self.invalid_times2:
                self.assertRaises(
                    InvalidTimeException, tow.__contains__, day + time
                )                                
            
        for time in self.times:    
            for day in self.invalid_days:
                self.assertRaises(
                    InvalidTimeOfWeekException, tow.__contains__, day + time
                )            
            for day in self.invalid_days2:
                self.assertRaises(
                    InvalidDayException, tow.__contains__, day + time
                )
                
        self.assertRaises(InvalidPeriodException, TimeOfWeek, '')
        self.assertRaises(InvalidPeriodException, TimeOfWeek, 'MON 1200-1700')
        self.assertRaises(InvalidPeriodException, TimeOfWeek, 'MON1200-1700, ')
        self.assertRaises(InvalidPeriodException, TimeOfWeek, 'MON1200-1700, TUE1000-1000')
        
        period = 'MON1200-1700,TUE1200-2359,HOL1000-1200'
        tow = TimeOfWeek(period)
        self.assertTrue('MON1200' in tow)
        self.assertTrue('TUE2358' in tow)
        self.assertTrue('HOL1200' in tow)
        self.assertFalse('MON1159' in tow)
        self.assertFalse('HOL0900' in tow)
        self.assertFalse('HOL1201' in tow)
        self.assertFalse('WED1201' in tow)
        self.assertFalse('THU1201' in tow)
        
        period = 'MON1200-1200'
        tow = TimeOfWeek(period)
        self.assertTrue('MON1200' in tow)
        self.assertFalse('MON1159' in tow)
        self.assertFalse('MON1201' in tow)
        
        tow = TimeOfWeek('MON1200-1300') + TimeOfWeek('TUE1400-1500')
        self.assertTrue('MON1200' in tow)
        self.assertTrue('TUE1400' in tow)
        
        #ensure adding works symmetrically
        tow = TimeOfWeek('TUE1400-1500') + TimeOfWeek('MON1200-1300')
        self.assertTrue('MON1200' in tow)
        self.assertTrue('TUE1400' in tow)
        
        tow = TimeOfWeek('MON1200-1300') + TimeOfWeek('MON0900-1500')
        self.assertTrue('MON1200' in tow)
        self.assertTrue('MON1159' in tow)
        self.assertFalse('MON0859' in tow)
        self.assertFalse('MON1501' in tow)
        
        tow = TimeOfWeek('MON1200-1700') + TimeOfWeek('MON0900-1300')
        self.assertTrue('MON1200' in tow)
        self.assertTrue('MON1159' in tow)
        self.assertTrue('MON1301' in tow)
        self.assertTrue('MON1700' in tow)
        self.assertFalse('MON0859' in tow)
        self.assertFalse('MON1701' in tow)
                        
        
        
                   
        

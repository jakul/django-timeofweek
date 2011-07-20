from django.test import TestCase
from timeofweek.util import TimeOfWeek
from timeofweek.exceptions import InvalidTimeOfWeekException,\
    InvalidDayException, InvalidTimeException, InvalidPeriodException


class TimeOfWeekTest(TestCase):
    
    def setUp(self):
        self.day_names = (
          'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN', 'HOL',
          'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'hol',
          'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Hol',
        )
        self.times = ('0000', '0920', '1200', '1545', '2359')

        self.invalid_days = ('M', 'T', 'monday', 'ananan')
        self.invalid_days2 = ('ABC', 'MOO')
        self.invalid_times = ('12345', '', '1', '123', '12', '-1', '1.2')
        self.invalid_times2 = ('3000', '9999', '1267')
        
        
        
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
                self.assertTrue(
                    day + time in tow, day+time + ' not in ' + str(tow)
                )
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
        self.assertRaises(InvalidPeriodException, TimeOfWeek, 'MON2359-2359')
        self.assertRaises(InvalidPeriodException, TimeOfWeek, 'MON1200-1200')
        self.assertRaises(InvalidTimeException, TimeOfWeek, 'MON2358-0000')
        self.assertRaises(InvalidPeriodException, TimeOfWeek, 'MON1200-1700, ')
        
        tow = TimeOfWeek('MON1200-1700,TUE1200-2359,HOL1000-1200')
        self.assertTrue('MON1200' in tow)
        self.assertTrue('TUE2358' in tow)
        self.assertTrue('HOL1159' in tow)
        self.assertFalse('MON1159' in tow)
        self.assertFalse('HOL0900' in tow)
        self.assertFalse('HOL1201' in tow)
        self.assertFalse('WED1201' in tow)
        self.assertFalse('THU1201' in tow)
        
        tow = TimeOfWeek('MON1200-1201')
        self.assertTrue('MON1200' in tow)
        self.assertFalse('MON1159' in tow)
        self.assertFalse('MON1201' in tow)

        tow = TimeOfWeek('MON2358-2400')
        self.assertTrue('MON2358' in tow)
        self.assertTrue('MON2359' in tow)
        def test_func(tow):
            return 'MON2400' in tow
        self.assertRaises(InvalidTimeException, test_func, tow)
        self.assertFalse('TUE0000' in tow)
        
        # Check spaces in input
        tow = TimeOfWeek(' M O N 1 2 0 0 -1 20 1,TU E 12 00 -13 00')
        self.assertTrue('MON1200' in tow)
        self.assertFalse('MON1159' in tow)
        self.assertFalse('MON1201' in tow)
        self.assertTrue('TUE1200' in tow)
        self.assertFalse('TUE1159' in tow)
        self.assertFalse('TUE1301' in tow)
        
        # Check addition        
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
        self.assertTrue('MON1659' in tow)
        self.assertFalse('MON0859' in tow)
        self.assertFalse('MON1701' in tow)
        
        # Test the 'minutes' property
        tow = TimeOfWeek()
        self.assertEqual(tow.minutes, 11520) #don't forget our week has 8 days
        
        # Ensure we don't get extra minutes by adding 2 together
        tow += TimeOfWeek()
        self.assertEqual(tow.minutes, 11520)
                        
        tow = TimeOfWeek('MON0000-0001')
        self.assertEqual(tow.minutes, 1)
        tow = TimeOfWeek('MON0000-0059')
        self.assertEqual(tow.minutes, 59)
        tow = TimeOfWeek('MON0000-0100')
        self.assertEqual(tow.minutes, 60)
        tow = TimeOfWeek('MON0000-0101')
        self.assertEqual(tow.minutes, 61)
        tow = TimeOfWeek('MON0000-2400')
        self.assertEqual(tow.minutes, 1440)
        tow = TimeOfWeek(
             'MON0000-1200,TUE0000-1200,WED0000-1200,THU0000-1200,FRI0000-1200,'
             'SAT0000-1200,SUN0000-1200,HOL0000-1200'
         )
        self.assertEqual(tow.minutes, 5760)
        
        
                   
        

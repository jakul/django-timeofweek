from timeofweek.exceptions import InvalidTimeOfWeekException,\
    InvalidDayException, InvalidTimeException, InvalidPeriodException,\
    InvalidTimePeriodException

class TimeOfWeek(object):
    """
    Stores a period of time within a week
    """
    _day_names = ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN', 'HOL')
    
    def __init__(self, tow=None):
        """
        Converts a string representing a time of week into a TimeOfWeek object.
        
        The time included include the start time and exclude the end time 
        """
        
        self._periods = {}
        if tow is None:
            for day_name in self._day_names:
                self._periods[day_name] = [0000, 2400]
        else:
            tow = tow.upper().replace(' ', '')
            periods = tow.split(',')
            for period in periods:
                day_name, start_time, end_time = self.__parse_period(period)
                self._periods[day_name] = (start_time, end_time)
                
    def __contains__(self, key):
        if key is None:
            return False
        
        key = key.upper().replace(' ', '')
        
        day, time = self.__parse_time(key)
        if not self._periods.has_key(day):
            #not valid at anytime on this day
            return False
        
        
        start_time, end_time = self._periods.get(day)

        if time < start_time or time >= end_time:
            #time is outside allowed bounds
            return False
        
        return True
    
    def __parse_time(self, tow):
        if len(tow) != 7:
            raise InvalidTimeOfWeekException(tow)
        
        day = tow[0:3]
        if day not in self._day_names:
            raise InvalidDayException(day)
    
        time = tow[3:]
        try:
            time = int(time)
        except (ValueError,):
            raise InvalidTimeException(time)
        
        if time < 0 or time > 2359:
            raise InvalidTimeException(time)
        
        if time % 100 > 59:
            raise InvalidTimeException(time)
        
        return day, time
    
    def __parse_period(self, period):
        if len(period) != 12:
            raise InvalidPeriodException(period)
        
        day = period[0:3]
        if day not in self._day_names:
            raise InvalidDayException(day)
    
        time_period = period[3:]
        if '-' not in time_period or len(time_period) != 9:
            raise InvalidTimePeriodException(time_period)
        
        start_time, end_time = time_period.split('-')
        
        try:
            start_time = int(start_time)
        except (ValueError,):
            raise InvalidTimeException(start_time)
        
        if start_time < 0 or start_time > 2359:
            raise InvalidTimeException(start_time)
        
        try:
            end_time = int(end_time)
        except (ValueError,):
            raise InvalidTimeException(end_time)
        
        if end_time <= 0 or end_time > 2400:
            raise InvalidTimeException(end_time)
        
        if end_time == start_time:
            raise InvalidPeriodException(period, 'Period contains 0 minutes')       

        return day, start_time, end_time
  
    def __add__(self, other):
        """
        Adds another TimeOfWeek to this one. If there is a period of the week
        which appears in either or both TimeOfWeeks then it will be in the
        return TimeOfWeek 
        """
        new_object = TimeOfWeek()
        new_object._periods = {}
        for day in other._periods:
            start_time, end_time = other._periods[day]
            if day in self._periods:
                if self._periods[day][0] < start_time:
                    start_time = self._periods[day][0]
                    
                if self._periods[day][1] > end_time:
                    end_time = self._periods[day][1]
                    
            new_object._periods[day] = (start_time, end_time)
            
        for day in self._periods:
            if day not in new_object._periods:
                new_object._periods[day] = self._periods[day]
                    
        return new_object
    
    def to_json(self):
        outputs = []
        for day_name in self._day_names:
            if day_name in self._periods:
                output = day_name + ''
                start_time, end_time = self._periods[day_name]
                output += '%04d-%04d' % (start_time, end_time)

                outputs.append(output)

        return ', '.join(outputs)
    
    @property
    def minutes(self):
        minutes = 0
        for start_time, end_time in self._periods.values():
            hours = start_time / 100
            minutes_ = start_time % 100
            finish = False
            while hours <= 23 and finish == False:
                while minutes_ <= 59 and finish == False:
                    time = hours * 100 + minutes_
                    if time >= end_time:
                        finish = True
                        continue
                    minutes += 1
                    minutes_ +=1
                hours += 1
                minutes_ = 0
                                    
        return minutes
    
    @property
    def has_holiday(self):
        return 'HOL' in self._periods
            
    def __str__(self):
        return self.to_json()
                
            
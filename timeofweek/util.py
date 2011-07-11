

class TimeOfWeek(object):
    """
    Stores a period of time within a week
    """
    
    _day_names = ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN', 'HOL')
    
    def __init__(self, tow=None):
        """
        Converts a string representing a time of week into a TimeOfWeek object 
        """
        
        self._days = {}
        for day_name in self._day_names:
            self._days[day_name] = [0000, 2359]
           
        if tow is not None: 
            periods = tow.split(',')
            for period in periods:
                start, stop = period.split('-')
                
            
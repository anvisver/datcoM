import math
import argparse

class Datetime_support:
    def time(self):
        """
        returns the (hour-minute-second) values of the datetime object
        """
        if self.rawtime < 0:
            self.charge = "-"
            self.rawtime = abs(self.rawtime)
        else:
            self.charge = "+"
        rawtime_without_leaps = self.rawtime - self.all_leap_days * self.time_units["d"]
        support = self.Backend(rawtime_without_leaps, "from_rawtime_to_datetime")
        hour, minute, second = support[3], support[4], support[5]
        rawtime_with_leaps = (
            hour * self.time_units["h"]
            + minute * self.time_units["M"]
            + second * self.time_units["s"]
        )
        self.rawtime = rawtime_with_leaps
        self.output = ["time", [0, 0, 0, hour, minute, second]]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self

    def date(self):
        """
        returns the (year-month-day) values of the datetime object
        """
        if self.rawtime < 0:
            self.charge = "-"
            self.rawtime = abs(self.rawtime)
        else:
            self.charge = "+"
        raw_no_leaps = self.rawtime - self.all_leap_days * self.time_units["d"]
        year, month, day, _, _, _ = self.Backend(raw_no_leaps, "from_rawtime_to_datetime")
        result, self.leap, self.all_leap_days = self.Backend(
            [year, month, day, 0, 0, 0], "from_rawtimeget_leapyears"
        )
        rawtime = 0.0
        for unit, value in zip(self.template, result):
            if unit == "m":
                for m in range(1, value):
                    rawtime += self.time_units["m"][m]
            elif unit == "d":
                if value >= 1:
                    rawtime += (value - 1) * self.time_units["d"]
            elif isinstance(self.time_units[unit], dict):
                for k in range(1, value + 1):
                    rawtime += self.time_units[unit][k]
            else:
                rawtime += value * self.time_units[unit]
        self.rawtime = rawtime
        self.output = ["date", [year, month, day, 0, 0, 0]]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self

    def year(self):
        if self.rawtime < 0:
            self.charge = "-"
            self.rawtime = abs(self.rawtime)
        else:
            self.charge = "+"
        
        raw_no_leaps = self.rawtime - self.all_leap_days * self.time_units["d"]
        year, _, _, _, _, _ = self.Backend(raw_no_leaps, "from_rawtime_to_datetime")
        self.rawtime = year * self.time_units["Y"] + self.all_leap_days * self.time_units["d"]
        self.output = ["year", [year, 0, 0, 0, 0, 0]]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self

    def month(self):
        if self.rawtime < 0:
            self.charge = "-"
            self.rawtime = abs(self.rawtime)
        else:
            self.charge = "+"
        raw_no_leaps = self.rawtime - self.all_leap_days * self.time_units["d"]
        _, month, _, _, _, _ = self.Backend(raw_no_leaps, "from_rawtime_to_datetime")
        result, self.leap, self.all_leap_days = self.Backend(
            [0, month, 0, 0, 0, 0], "from_rawtimeget_leapyears"
        )
        rawtime = 0.0
        for unit, value in zip(self.template, result):
            if unit == "m":
                for m in range(1, value):
                    rawtime += self.time_units["m"][m]
            elif unit == "d":
                rawtime += value * self.time_units["d"]
            elif isinstance(self.time_units[unit], dict):
                for k in range(1, value + 1):
                    rawtime += self.time_units[unit][k]
            else:
                rawtime += value * self.time_units[unit]
        self.rawtime = rawtime
        self.output = ["month", [0, month, 0, 0, 0, 0]]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self

    def day(self):
        if self.rawtime < 0:
            self.charge = "-"
            self.rawtime = abs(self.rawtime)
        else:
            self.charge = "+"
        raw_no_leaps = self.rawtime - self.all_leap_days * self.time_units["d"]
        _, _, day, _, _, _ = self.Backend(raw_no_leaps, "from_rawtime_to_datetime")
        self.rawtime = (day - 1) * self.time_units["d"]
        self.output = ["day", [0, 0, day, 0, 0, 0]]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self

    def hour(self):
        """
        returns the (hour) values of the datetime object
        """
        if self.rawtime < 0:
            self.charge = "-"
            self.rawtime = abs(self.rawtime)
        else:
            self.charge = "+"
        raw_no_leaps = self.rawtime - self.all_leap_days * self.time_units["d"]
        _, _, _, hour, _, _ = self.Backend(raw_no_leaps, "from_rawtime_to_datetime")
        self.rawtime = hour * self.time_units["h"]
        self.output = ["hour", [0, 0, 0, hour, 0, 0]]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self

    def minute(self):
        """
        returns the (minute) values of the datetime object
        """
        if self.rawtime < 0:
            self.charge = "-"
            self.rawtime = abs(self.rawtime)
        else:
            self.charge = "+"
        raw_no_leaps = self.rawtime - self.all_leap_days * self.time_units["d"]
        _, _, _, _, minute, _ = self.Backend(raw_no_leaps, "from_rawtime_to_datetime")
        self.rawtime = minute * self.time_units["M"]
        self.output = ["minute", [0, 0, 0, 0, minute, 0]]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self

    def second(self):
        """
        returns the (second) values of the datetime object
        """
        if self.rawtime < 0:
            self.charge = "-"
            self.rawtime = abs(self.rawtime)
        else:
            self.charge = "+"
        raw_no_leaps = self.rawtime - self.all_leap_days * self.time_units["d"]
        _, _, _, _, _, second = self.Backend(raw_no_leaps, "from_rawtime_to_datetime")
        self.rawtime = second * self.time_units["s"] 
        self.output = ["second", [0, 0, 0, 0, 0, second]]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self

    def offset(self):
        self.rawtime = 0
        self.output = ["fulldatetime", [0, 0, 0, 0, 0, 0]]
        return self
class Maths_Support:
    """
    Maths_Support class meant to give main-class datetime flexibility when it comes to mathematical operations
    """
    def __init__(self, rawtime):
        self.rawtime = rawtime

    def __add__(self, other):
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime + other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime + other)
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __sub__(self, other):
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime - other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime - other)
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __mul__(self, other):
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime * other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime * other)
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __truediv__(self, other):
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime / other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime / other)
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __floordiv__(self, other):
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime // other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime // other)
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __mod__(self, other):
        if isinstance(other, Maths_Support):
            return self.rawtime % other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime % other
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __pow__(self, other):
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime ** other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime ** other)
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __eq__(self, other):
        if isinstance(other, Maths_Support):
            return self.rawtime == other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime == other
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __gt__(self, other):
        if isinstance(other, Maths_Support):
            return self.rawtime > other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime > other
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __ge__(self, other):
        if isinstance(other, Maths_Support):
            return self.rawtime >= other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime >= other
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __lt__(self, other):
        if isinstance(other, Maths_Support):
            return self.rawtime < other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime < other
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __le__(self, other):
        if isinstance(other, Maths_Support):
            return self.rawtime <= other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime <= other
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __ne__(self, other):
        if isinstance(other, Maths_Support):
            return self.rawtime != other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime != other
        return DatconError(False,[self,other],"unregistered operation","Maths_Support",True)

    def __repr__(self):
        return DatconError(False,[self.rawtime],"unregistered operation","Maths_Support",True)
class datetime(Maths_Support,Datetime_support):
    """
    Datcon: A Python library for datetime manipulation and math operations.
    This library allows you to create, manipulate, and perform mathematical operations on datetime objects.
    It supports various formats and provides a simple interface for datetime operations.
    It is designed to be easy to use and flexible, making it suitable for a wide range of applications.     
    
    📘 datetime Help Manual 📘
    ===========================

    🧱 Initialization
    -----------------
    datetime()
        Creates an empty datetime object. This is the root of all datetime operations.

    🕰️ Time & Date Extraction
    --------------------------
    These instance methods extract parts of the datetime object and update the `output` accordingly.

    .date()
        📅 Returns (year, month, day)

    .time()
        ⏰ Returns (hour, minute, second)

    .year()
        🗓️ Returns year only

    .month()
        🌙 Returns month only

    .day()
        📆 Returns day only

    .hour()
        🕐 Returns hour only

    .minute()
        🕑 Returns minute only

    .second()
        ⏱️ Returns second only

    🧮 Math & Offsets
    -----------------
    .Offset()
        🔄 Resets the current datetime object to zero (clears everything)

    Math Operations:
        The datetime class supports arithmetic and comparisons:
            a + b       -> Add two datetime rawtimes
            a - b       -> Subtract one datetime from another
            a * 2       -> Multiply rawtime by a number
            a == b      -> Compare if two datetimes are equal
            a < b, >, <=, >=   -> All standard comparisons work

    🧩 Datetime Creation
    --------------------
    These class methods create datetime objects from different kinds of input.

    strptime(value: str, template: str)
        🧵 Parses a formatted string into a datetime object
        Example:
            dt.strptime("2024-12-31 23:59:59", "%Y-%m-%d %H:%M:%S")

    intptime(value: list[int], template: str)
        🧮 Parses a list of integers into a datetime object using a format string
        Example:
            dt.intptime([2024, 12, 31, 23, 59, 59], "%Y%m%dHMS")

    operand(rawtime: float)
        🔢 Converts a rawtime float (internal representation) into a full datetime object
        Useful for datetime math:
            dt.operand(dt1.rawtime + dt2.rawtime)

    📤 Output / Display
    -------------------
    str(obj)
        🖨️ Converts the current output of the datetime object into a readable string
        Output depends on last method used:
            - (2024-12-31 23:59:59)
            - (2024)
            - (12)
            - (23:59:59)

    📜Final Notes:
    -------------------

    to open help write in the terminal one of the following options:
        -Python3 datcon.py -h 
        -Python3 datcon.py --help

    """
    def __init__(self):    
        self.time_units = {
            "Y": 31536000,    
            "m": {
            1: 2678400,
            2: 2419200,
            3: 2678400,
            4: 2592000,
            5: 2678400,
            6: 2592000,
            7: 2678400,
            8: 2678400,
            9: 2592000,
            10: 2678400,
            11: 2592000,
            12: 2678400},   
            "d": 86400,      
            "h": 3600,      
            "M": 60,          
            "s": 1,                  
        }

        self.rawtime = float(0)
        self.template = ['Y', 'm', 'd', 'h', 'M', 's']
        self.leap=False
        self.all_leap_days=int(0)
        self.output = False
        self.charge = "+"
    def __str__(self):

        source = self.output[0]
        data = self.output[1]
        year = int(data[0])
        month = int(data[1])
        day = int(data[2])
        hour = int(data[3])
        minute = int(data[4])
        second = float(data[5])

        if self.charge == "-":
            orion = "B.C"
        else:
            orion = "A.C"

        if math.floor(second) == second:
            decimal = int
        else:
            decimal = float

        if source == "fulldatetime":
            return f"({int(year):04}-{int(month):02}-{int(day):02} {int(hour):02}:{int(minute):02}:{decimal(second):02}) {orion}"

        elif source == "date":
            return f"({int(year):04}-{int(month):02}-{int(day):02}) {orion}"
        elif source == "time":
            return f"({int(hour):02}:{int(minute):02}:{decimal(second):02}) {orion}"
        elif source == "year":
            return f"({int(year):04}) {orion}"
        elif source == "month":
            return f"({int(month):02}) {orion}"
        elif source == "day":
            return f"({int(day):02}) {orion}"
        elif source == "hour":
            return f"({int(hour):02}) {orion}"
        elif source == "minute":
            return f"({int(minute):02}) {orion}"
        elif source == "second":
            return f"({decimal(second):02}) {orion}"
        else:
            return "No source Found"
    @classmethod
    def strptime(cls, value: str, template: str):
        """
        requires a value:str and a template:str\n
        generates a datetime object out of thoes\n
        """
        self = cls()

        #before or after Christ
        if value[0] == "-" or value[0] == "+":
            self.charge = value[0]
            value = value[1:]
        else:
            self.charge = "+"

        if not isinstance(value, str):
            DatconError(template, value, "uncorrect value", "strptime", True)

        stemplate = []
        corrector = {"y":"Y","D":"d","H":"h","S":"s"}


        
        for item in template:
            if item not in  ["%","f"]:
                if item in corrector:
                    if corrector[item] not in stemplate:
                        stemplate.append(corrector[item])
                elif item in ["Y","d","h","s","m","M"]:
                    if item not in stemplate:
                        stemplate.append(item)

        svalue = []
        exec1 = ""
        for item in value:

            if item in ["1","2","3","4","5","6","7","8","9","0","."]:     #normal number adding
                exec1+=item

            else:       #well, number break I guess?
                try:
                    svalue.append(float(exec1))
                    exec1 = ""

                except ValueError:
                    try:
                        if "." in exec1:
                            exec1.replace(".","") 
                            svalue.append(float(exec1[0]))
                            svalue.append(float(exec1[1]))
                        else:
                            svalue.append(float(exec1))
                    except ValueError:
                        exec1 = ""
        
        if exec1 and len(svalue) <len(stemplate):     
            svalue.append(float(exec1))

        if len(stemplate) > len(svalue):
            DatconError(stemplate,svalue,"duplicated parameters","strptime",True)
        elif len(stemplate) < len(svalue):
            DatconError(stemplate,svalue,"too many values","strptime",True)
        answer = []
        j = 0

        for i in range(len(self.template)):

            if self.template[i] == stemplate[j]:
                
                answer.append(svalue[j])
                # advance to the next token if there are any left
                if j < len(stemplate) - 1:
                    j += 1
            else:
                answer.append(0)


        exact_datetime = answer


        support = self.Backend(exact_datetime,"from_rawtimeget_leapyears")
        
        result = support[0]
        self.leap = support[1]
        self.all_leap_days = support[2]

        rawtime = float(0)

        idx_day   = self.template.index("d")
        idx_month = self.template.index("m")
        idx_year  = self.template.index("Y")
        result[idx_day]   +=1
        result[idx_month] +=1
        result[idx_year]  +=1

        if self.leap:
            self.time_units["m"][2] = 2505600
        

        for i in range(len(self.template)):
            unit = self.template[i]
            value = result[i]
            if unit == "m":
                for m in range(1, int(value)):
                    rawtime += self.time_units["m"][m]
            elif unit == "d":
                rawtime += (value - 1) * self.time_units["d"]
            elif isinstance(self.time_units[unit], dict):
                for k in range(1, value + 1):
                    rawtime += self.time_units[unit][k]
            else:
                rawtime += value * self.time_units[unit]
        if self.leap:
            self.time_units["m"][2] = 2419200

 
 

        self.rawtime = rawtime
        rawtime_without_leaps = rawtime - self.all_leap_days * self.time_units["d"]
        support = self.Backend(rawtime_without_leaps,"from_rawtime_to_datetime",self.leap)
        self.output = ["fulldatetime",support]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self
    @classmethod
    def intptime(cls,value:list[int],template:str):
        """
        requires a value:list[int] and a template:str\n

        generates a datetime object out of thoes\n
        in case of error: check whether the value was introduced inside of a list\n

        """
        self = cls()
        if  value[0] == "-":
            self.charge = value[0]
            value = value[1:]
        elif value[0] == "+":
            self.charge = value[0]
            value = value[1:]
        else:
            self.charge = "+"

        for item in value:
            if not isinstance(item, (int,float)):
                DatconError(template,value,"uncorrect input value","intptime",True)
            
        if "f" in template:
            template = DatconError(template,value, "f in template","intptime",False)


        
        parameters = []
        for item in template:
            if item in self.time_units:
                parameters.append(item)


        if len(parameters) > len(value):
            DatconError(template,value,"duplicated parameters","intptime",True)
        elif len(parameters) < len(value):
            DatconError(template,value,"too many values","intptime",True)
        answer = []
        j = 0
        for i in range(0,len(self.template)):
            if self.template[i] == parameters[j]:
                
                answer.append(value[j])
                if len(parameters)>j:
                    j+=1
            else:
                answer.append(0)

        exact_datetime = answer   

        support = self.Backend(exact_datetime,"from_rawtimeget_leapyears")

        result = support[0]
        self.leap = support[1]
        self.all_leap_days = support[2]

        rawtime = float(0)

        idx_day   = self.template.index("d")
        idx_month = self.template.index("m")
        idx_year  = self.template.index("Y")
        result[idx_day]   +=1
        result[idx_month] +=1
        result[idx_year]  +=1

        if self.leap:
            self.time_units["m"][2] = 2505600
        for i in range(len(self.template)):
            unit = self.template[i]
            value = result[i]
            if unit == "m":
                for m in range(1, value):
                    rawtime += self.time_units["m"][m]
            elif unit == "d":
                rawtime += (value - 1) * self.time_units["d"]
            elif isinstance(self.time_units[unit], dict):
                for k in range(1, value + 1):
                    rawtime += self.time_units[unit][k]
            else:
                rawtime += value * self.time_units[unit]
        rawtime_without_leaps = rawtime - self.all_leap_days*self.time_units["d"]

        self.rawtime = rawtime
        if self.leap:
            self.time_units["m"][2] = 2419200
        support = self.Backend(rawtime_without_leaps,"from_rawtime_to_datetime",self.leap)
        self.output = ["fulldatetime",support]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self
    @classmethod
    def operand(cls, rawtime):
        """
        "operand(rawtime: float) ->\n
        datetime: Converts a raw-seconds value (with leap-days normalized out) back into a full datetime,\n
        correctly handling Feb 29 on leap years. Returns a new datetime instance with its\n
        output set to [‘fulldatetime’, [Y, M, D, h, m, s]]."

        """
        self = cls()
        _, self.leap, self.all_leap_days = cls.Backend(rawtime, "find_leapvalue_in_rawtime")

        if f"{rawtime}"[0] == "-":
            self.charge = f"{rawtime}"[0]
            rawtime = abs(rawtime)
        else:
            self.charge = "+"

        raw_no_leaps = rawtime - self.all_leap_days * self.time_units["d"]
        final_parts  = cls.Backend(raw_no_leaps,"from_rawtime_to_datetime",self.leap)

        self.output  = ["fulldatetime", final_parts]
        self.rawtime = rawtime
        return self
    @classmethod
    def datetime(cls, value:list):
        """
        Generates a datetime object from a list or tuple of numbers.\n
        The interpretation starts from the biggest unit (e.g., year, month...)
        
        """
        
        self = cls()
        template = self.template
        if value[0] == "-":
            self.charge = value[0]
            value = value[1:]
        elif value[0] == "+":
            self.charge = value[0]
            value = value[1:]
        else:
            self.charge = "+"
        
        for item in value:
            if not isinstance(item, (int,float)):
                DatconError(template,value,"uncorrect input value","datetime",True)
        if len(value)>len(template):
            DatconError(template,value,"too many values","datetime.datetime",True)
        
        support = []
        for i in range(len(template)):
            try:
                support.append(value[i])
            except IndexError:
                support.append(0)

        support=self.Backend(support,"from_rawtimeget_leapyears")

        self.all_leap_days=support[2]
        self.leap=support[1]
        rawtime = float(0)
        result = support[0]
        
        idx_day   = self.template.index("d")
        idx_month = self.template.index("m")
        idx_year  = self.template.index("Y")
        result[idx_day]   +=1
        result[idx_month] +=1
        result[idx_year]  +=1
        if self.leap:
            self.time_units["m"][2] = 2505600 

        for i in range(len(self.template)):
            unit = self.template[i]
            value = result[i]
            if unit == "m":
                for m in range(1, value):
                    rawtime += self.time_units["m"][m]
            elif unit == "d":
                rawtime += (value - 1) * self.time_units["d"]
            elif isinstance(self.time_units[unit], dict):
                for k in range(1, value + 1):
                    rawtime += self.time_units[unit][k]
            else:
                rawtime += value * self.time_units[unit]
        if self.leap:
            self.time_units["m"][2] = 2419200 
        self.rawtime = rawtime
        rawtime_without_leaps = rawtime - self.all_leap_days * self.time_units["d"]
        support = self.Backend(rawtime_without_leaps,"from_rawtime_to_datetime",self.leap)
        self.output = ["fulldatetime",support]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self
    @classmethod
    def timedate(cls, value: list):
        """
        Generates a datetime object from a list or tuple of numbers.\n
        The interpretation starts from the smallest unit (e.g., seconds, minutes...)
        """
        
        self = cls()

        if value[0] == "-":
            self.charge = value[0]
            value = value[1:]
        elif value[0] == "+":
            self.charge = value[0]
            value = value[1:]
        else:
            self.charge = "+"
        
        for item in value:
            if not isinstance(item, (int,float)):
                DatconError(False,value,"uncorrect input value","timedate",True)
        # Reversess the template 
        template = list(reversed(self.template))

        if len(value) > len(template):
            DatconError(template, value, "too many values", "datetime.datetime", True)


        support = []
        for i in range(len(template)):
            try:
                support.append(value[i])
            except IndexError:
                support.append(0)

        # Reverse support 
        support = list(reversed(support))

        support = self.Backend(support, "from_rawtimeget_leapyears")

        self.all_leap_days = support[2]
        self.leap = support[1]
        rawtime = float(0)
        result = support[0]

        idx_day   = self.template.index("d")
        idx_month = self.template.index("m")
        idx_year  = self.template.index("Y")
        result[idx_day]   +=1
        result[idx_month] +=1
        result[idx_year]  +=1
        
        if self.leap:
            self.time_units["m"][2] = 2505600
        for i in range(len(self.template)):
            unit = self.template[i]
            value = result[i]
            if unit == "m":
                for m in range(1, value):
                    rawtime += self.time_units["m"][m]
            elif unit == "d":
                rawtime += (value - 1) * self.time_units["d"]
            elif isinstance(self.time_units[unit], dict):
                for k in range(1, value + 1):
                    rawtime += self.time_units[unit][k]
            else:
                rawtime += value * self.time_units[unit]
        if self.leap:
            self.time_units["m"][2] = 2419200

        self.rawtime = rawtime
        rawtime_without_leaps = rawtime - self.all_leap_days * self.time_units["d"]
        support = self.Backend(rawtime_without_leaps, "from_rawtime_to_datetime", self.leap)
        self.output = ["fulldatetime", support]
        if self.charge == "-":
            self.rawtime = -self.rawtime
        return self   
    @classmethod
    def Backend(cls,value,task:str,leap:bool = None):
        """
        programs are run in the back end with the objective to \n
        not take up speace and be easily replicated across methods
        """
        self = cls()
        if task =="from_rawtimeget_leapyears":
            year = value[0]
            month = value[1]
            day = value[2]

            hour = value[3]
            minute = value[4]
            second = value[5]
            while second >= 60:
                second -= 60
                minute += 1
            while minute >= 60:
                minute -= 60
                hour += 1
            while hour >= 24:
                hour -= 24
                day += 1

            if month in [1, 3, 5, 7, 8, 10, 12]:
                # Months with 31 days
                while day > 31:
                    day -= 31
                    month += 1
            elif month in [4, 6, 9, 11]:
                while day > 30:
                    day -= 30
                    month += 1
            elif month == 2:
                if self.leap:
                    while day > 29:
                        day -= 29
                        month += 1
                else:
                    while day > 28:
                        day -= 28
                        month += 1
            while month>12:
                month-=12
                year+=1
            



            extra = 0
            self.leap = False
            if year % 4 == 0:
                    if year % 100 == 0:
                        if year % 400 == 0:
                            self.leap = True
                    else:
                        self.leap=True

            for time in range(1, int(year) + 1):

                if time % 4 == 0:
                    if time % 100 == 0:
                        if time % 400 == 0:
                            extra += 1 

                    else:
                        extra += 1  
                        
            

                
            self.all_leap_days=extra

            return [[year,month,day+extra,hour,minute,second,],self.leap,extra] 
        if task == "from_rawtime_to_datetime":
            if leap:
                self.time_units["m"][2] = 2505600 
            rawtime = value 

            year = int(math.floor(rawtime / self.time_units["Y"])) 
            rawtime = rawtime % self.time_units["Y"]
            month = 1
            while month < 13 and rawtime >= self.time_units["m"][month]:
                rawtime -= self.time_units["m"][month]
                month += 1
            month = min(month, 12)
            
            day = 1
            while rawtime >= self.time_units["d"]:
                rawtime -= self.time_units["d"]
                day += 1
            
            hour = 0
            while rawtime >= self.time_units["h"]:
                hour += 1
                rawtime -= self.time_units["h"]

            minute = 0
            while rawtime >= self.time_units["M"]:
                minute += 1
                rawtime -= self.time_units["M"]

            
            second = round(rawtime,4)
            if self.leap:
                self.time_units["m"][2] = 2419200
            return [year,month,day,hour,minute,second]
        elif task == "find_leapvalue_in_rawtime":

            year_guess = int(math.floor(value / cls().time_units["Y"]))
            year = max(year_guess, 1)
            leap_flag = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
            all_leaps = 0
            for t in range(1, year):
                if t%4==0 and (t%100!=0 or t%400==0):
                    all_leaps += 1
            raw_no_leaps = value - all_leaps * cls().time_units["d"]


            date_parts = cls.Backend(raw_no_leaps, "from_rawtime_to_datetime", leap_flag)

            support    = cls.Backend(date_parts, "from_rawtimeget_leapyears")
            all_leaps  = support[2]
            leap = support[1]

            return [date_parts, leap, all_leaps]


        else:
            raise ValueError("Unknown task")
def DatconError(template:False,value:False,type,pleace:False,critical:False):
    
    if type == "uncorrect value":
        print(f"Datcon: there was an error in {pleace} , the input value was uncorrect")
    elif type == "duplicated parameters":
        print(f"Datcon: There are duplicated parameters in your {pleace} function, pls check the template: {template}")
    elif type == "uncorrect input value":
        if pleace in [ "intptime","datetime","timedate"]:
            support = "a list or a tuple, \n\tit must be composed of integers or floats \n\texcept the first element which can be a string - to indicate B.C"
        elif pleace == "strptime":
            support = "inside a string"
        print(f"Datcon: the input value of {pleace} must always be {support}")
    elif type == "f in template":
        print("Datcon: in this version of Datcon,we have already removed the f,we politly request the usser to refrain from ussing it from now ")
    elif type == "too many values":
        print(f"Datcon:there where to many values in your {pleace} function, pls check the value {value}")
    elif type == "unregistered operation":
        print("we runned into an error when it came to executing complex operations with datetime objects")
    if critical:
        return exit()

    if type == "f in template":
        template.replace("f", "")
        return template
if __name__ == "__main__":
    parser = argparse.ArgumentParser(datetime.__doc__)
    args = parser.parse_args()
    # Example usage


__all__ = ["datetime","Maths_Support","Datetime_support","DatconError"]
#!bin cant remember the full stuff I had to write here srry
from __future__ import annotations
from enum import Enum
__all__ = ["datetime", "datetime_support", "Maths_Support","AC","BC", "EpochType"]
class EpochType(Enum):
    AC = "ac"  # After Christ (default)
    BC = "bc"  # Before Christ
# Export enum for easier external use
AC = EpochType.AC
BC = EpochType.BC
class Maths_Support:
    """
    Maths_Support provides arithmetic and comparison operations based on rawtime,
    enabling datetime objects to support intuitive math operations directly.

    These operations act upon the `rawtime` attribute, which represents time in seconds
    from a defined epoch.
    """
    def __init__(self, rawtime:float) -> datetime:
        self.rawtime = rawtime
    def __add__(self, other) -> datetime:
        """
        Add a scalar value (seconds) or another datetime's rawtime to this instance.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime + other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime + other)
		#RAISE ISSUE 
    def __sub__(self, other) -> datetime:
        """
        Subtract a scalar or another datetime's rawtime from this instance.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime - other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime - other)
		#RAISE ISSUE 
    def __mul__(self, other) -> datetime:
        """
        Multiply this instance's rawtime with a scalar or another datetime's rawtime.
        Useful for scaling durations.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime * other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime * other)
		#RAISE ISSUE 
    def __truediv__(self, other) -> datetime:
        """
        Perform true division of this instance's rawtime by a scalar or another rawtime.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime / other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime / other)
		#RAISE ISSUE 
    def __floordiv__(self, other) -> datetime:
        """
        Perform floor division on rawtime.
        Rounds down the result to the nearest integer.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime // other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime // other)
		#RAISE ISSUE 
    def __mod__(self, other) -> datetime:
        """
        Return the remainder after dividing rawtime by scalar or another rawtime.
        Useful for measuring periodic cycles.
        Returns a float.
        """
        if isinstance(other, Maths_Support):
            return self.rawtime % other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime % other
		#RAISE ISSUE 
    def __pow__(self, other) -> datetime:
        """
        Raise rawtime to a given power (scalar or another rawtime).
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime ** other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime ** other)
		#RAISE ISSUE 
    # Comparison operations return boolean values
    def __eq__(self, other) -> datetime:
        """Check equality between this instance and another rawtime or scalar."""
        if isinstance(other, Maths_Support):
            return self.rawtime == other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime == other
		#RAISE ISSUE 
    def __gt__(self, other) -> datetime:
        """Greater-than comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime > other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime > other
		#RAISE ISSUE 
    def __ge__(self, other) -> datetime:
        """Greater-than-or-equal-to comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime >= other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime >= other
		#RAISE ISSUE 
    def __lt__(self, other) -> datetime:
        """Less-than comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime < other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime < other
		#RAISE ISSUE 
    def __le__(self, other) -> datetime:
        """Less-than-or-equal-to comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime <= other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime <= other
		#RAISE ISSUE 
    def __ne__(self, other) -> datetime:
        """Check inequality between this instance and another."""
        if isinstance(other, Maths_Support):
            return self.rawtime != other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime != other
		#RAISE ISSUE 
    def __repr__(self,other = None) -> None:
        """
        Prevent accidental use of __repr__ unless implemented explicitly.
        Triggers a DatconError to force conscious developer decisions.
        """
		#RAISE ISSUE 
class datetime_support:

    def __init__(self):
        self.data = self.output [0]
        self.source = self.output[1]
        self.converter = 0
    @property
    def _convert_to_(self):
        self.converter = 1
        return self
    @property
    def _object_only_accounts_for_(self):
        self.converter = 2
        return self

    @property
    def year(self) -> datetime | float | int:
        
        def is_leap_year(year):
            """Return True if year is a leap year in the Gregorian calendar."""
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        def seconds_in_year(year):
            """Return number of seconds in the given year."""
            days = 366 if is_leap_year(year) else 365
            return days * 24 * 60 * 60
        def seconds_to_exact_years(seconds):
            """Convert seconds into exact years, considering leap years."""
            years_passed = 0
            year = 0

            while seconds >= seconds_in_year(year):
                seconds -= seconds_in_year(year)
                year += 1
                years_passed += 1

            fraction_of_year:float | int = seconds / seconds_in_year(year)
            total_years = years_passed + fraction_of_year

            return total_years
        if self.converter == 1:
            return seconds_to_exact_years(self.rawtime)
        elif self.converter == 2:
            return datetime.datetime([self.data[0]])
        return float(self.data[0])
    @property  
    def month(self) -> datetime | float | int:

        def is_leap_year(year):
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        def days_in_month(year, month):
            """Return number of days in a given month of a given year."""
            if month in {1, 3, 5, 7, 8, 10, 12}:
                return 31
            elif month in {4, 6, 9, 11}:
                return 30
            elif month == 2:
                return 29 if is_leap_year(year) else 28
            else:
                raise ValueError("Month must be 1..12")
        def seconds_in_month(year, month):
            return days_in_month(year, month) * 24 * 60 * 60
        def seconds_to_exact_months(seconds):
            """
            Convert seconds into exact months, considering leap years and month lengths.
            Starts counting from (year=0, month=0).
            """
            year, month = 0, 1  # start at "year 0, month 1"
            months_passed = 0

            while seconds >= seconds_in_month(year, month):
                seconds -= seconds_in_month(year, month)
                months_passed += 1
                # Increment month/year
                month += 1
                if month > 12:
                    month = 1
                    year += 1

            # Fraction of current month
            fraction_of_month = seconds / seconds_in_month(year, month)
            total_months = months_passed + fraction_of_month

            return total_months 
        if self.converter == 1:
            return seconds_to_exact_months(self.rawtime)
        elif self.converter == 2:
            return datetime.datetime([1,self.data[1]])
        return float(self.data[1])
    @property
    def day(self) ->datetime | float | int:
        def seconds_to_days(seconds: float) -> float:
            SECONDS_PER_DAY = 24 * 60 * 60  # 86400
            return seconds / SECONDS_PER_DAY
        if self.converter == 1:
            return seconds_to_days(self.rawtime)
        elif self.converter == 2:
            return datetime.datetime([0,0,self.data[2]])
        return float(self.data[2])
    @property
    def hour(self) ->datetime | float | int:
        if self.converter == 1:
            return self.rawtime/3600
        if self.converter == 2:
            return datetime.datetime([1,1,1,self.data[3]])
        return float(self.data[3])
    @property
    def minute(self) ->datetime | float | int:
        if self.converter == 1:
            return self.rawtime / 60
        elif self.converter == 2:
            return datetime.datetime([1,1,1,0,self.data[4]])
        return float(self.data[4])
    @property
    def second(self) ->datetime | float | int:
        if self.converter == 1:
            return self.rawtime
        elif self.converter == 2:
            return datetime.datetime([1,1,1,0,0,self.data[5]])
        return float(self.data[5])
    @property
    def time(self) -> datetime | list[int | float] | float | int:
        if self.converter == 1:
            return self.hour*self.minute*self.second
        elif self.converter == 2:
            return datetime.datetime([1,1,1,self.data[3],self.data[4],self.data[5]])
        return self.data[0:3]
    @property
    def date(self) -> datetime | list[int] | float | int:
        if self.converter == 1:
            return self.year*self.month*self.day
        elif self.converter == 2:
            return datetime.datetime([self.data[0],self.data[1],self.data[2]])
        return self.data[3:6]
class datetime(Maths_Support,datetime_support):

    TIME_UNITS:dict[str,int] = {
            "y": 31536000,
            "m": {
                1: 2678400, 2: 2419200, 3: 2678400, 4: 2592000,
                5: 2678400, 6: 2592000, 7: 2678400, 8: 2678400,
                9: 2592000, 10: 2678400, 11: 2592000, 12: 2678400},
            "d": 86400,
            "h": 3600,
            "mi": 60,
            "s": 1,
        }
    _SENTINEL_VALUE_: object = object()
    CENTRAL_EUROPEAN_TIMELINE:int = int(7200)

    def __init__(self,rawtime:float | int = 0,template:str = ['y', 'm', 'd', 'h', 'mi', 's'],anchor:float | int = 0,output:list = [None,None]):
        self.rawtime:float | int = rawtime
        self.anchor:float | int = anchor
        self.converter = 0
        
        self.template:str = template
        self.output:list = output
        self.epoch_type = AC if rawtime >= 0 else BC

    def __str__(self) -> datetime :
        data, source = self.output

        Y, M, D, h, mi, s = data

        sec = int(s) if float(s).is_integer() else float(s)

        if self.converter != 0:
            #RAISE ISSUE
            pass

        # Determine self.epoch_type.name and adjusted values based on calendar mode and rawtime

        # Format string based on source type
        if source == "fulldatetime":
            return f"({Y:04}-{M:02}-{D:02} {h:02}:{mi:02}:{sec:02}){self.epoch_type.name}"
        elif source == "date":
            return f"({Y:04}-{M:02}-{D:02}) {self.epoch_type.name}"
        elif source == "time":
            return f"({h:02}:{mi:02}:{sec:02}) {self.epoch_type.name}"
        elif source == "year":
            return f"({Y:04}) {self.epoch_type.name}"
        elif source == "month":
            return f"({M:02}) {self.epoch_type.name}"
        elif source == "day":
            return f"({D:02}) {self.epoch_type.name}"
        elif source == "hour":
            return f"({h:02}) {self.epoch_type.name}"
        elif source == "minute":
            return f"({mi:02}) {self.epoch_type.name}"
        elif source == "second":
            return f"({sec:02}) {self.epoch_type.name}"
        else:
            return "No source Found"
    @classmethod
    def operand(cls, base_rawtime: datetime | float | int,*, anchor_date: datetime | float | int = 0,reverse: bool = False) :
        """
        Treat `base_rawtime` as seconds from the epoch, optionally subtracting an anchor.
        If `reverse=True`, flips the sign of `base_rawtime`.
        
        Returns a new datetime object with the correct epoch and rawtime.
        """
        self = cls()

        # If base_rawtime is a datetime instance, extract its rawtime
        if isinstance(base_rawtime, datetime):
            base_rawtime = base_rawtime.rawtime

        # 1) Convert anchor_date to a float seconds value
        anchor_sec = self.anchor_converter(anchor_date)

        # 2) Apply reverse flag if needed
        if reverse:
            base_rawtime = -base_rawtime

        # 3) Compute absolute rawtime: seconds since epoch
        absolute_rawtime = base_rawtime - anchor_sec

        # 4) Determine epoch type (AC / BC) and magnitude for display
        if absolute_rawtime < 0:
            era = BC
            secs = abs(absolute_rawtime)
        else:
            era = AC
            secs = absolute_rawtime

        # 5) Convert seconds into full [Y, M, D, h, i, s]
        parts = self.convert_rawtime_to_date(secs)

        # 6) Fill instance and return
        self.rawtime = absolute_rawtime
        self.epoch_type = era
        self.output = [parts, "fulldatetime"]
        self.anchor = anchor_sec
        return self
    @classmethod
    def stamp(cls, input_value: list[int] | str = [0,1,1,0,0,0],input_template: list[str] | str = ['y', 'm', 'd', 'h', 'mi', 's'], epoch_type: EpochType = AC,*, anchor_date: datetime | float | int = 0) :
        self = cls() # creates an instance
        self.anchor = self.anchor_converter(anchor_date)
        value, self.template = self.value_template_extractor(input_value,input_template)
        if len(value)>6 or len(self.template)>6:
            #RAISE ISSUE    
            pass
        if len(value) < len(self.template):
            #RAISE ISSUE
            pass
        return self.finalize_full_datetime(value,epoch_type)
    @classmethod
    def datetime(cls, input_value: datetime | list[int] | str = [0,1,1,0,0,0], epoch_type: EpochType = AC,*, anchor_date: datetime | float | int = 0,template_reverse = False):
        """
        creates a datetime object ussing the inputted values while autofilling in case of a lack of does,\n
        by default it follows the `[year,month,day,hour,minute,second]` sequence,\n
        if template_reverse is active, it will go from seconds to years instead 
        """
        self = cls() # creates an instance

        template = ['y', 'm', 'd', 'h', 'mi', 's'][::-1] if template_reverse else ['y', 'm', 'd', 'h', 'mi', 's']

        self.anchor = self.anchor_converter(anchor_date)
        value, self.template = self.value_template_extractor(input_value,template)

        if len(value)>6 or len(value) < 6:
            #RAISE ISSUE    
            pass
        return self.finalize_full_datetime(value,epoch_type)
    @classmethod
    def current_time(cls,*, anchor_date: float | int = 0) -> datetime:
        """
        Returns the current real-world UTC time as [Y, m, d, h, i, s],\n
        adds the anchor_date, `datetime may be passed as an anchor`
        """
        import time
        raw = time.localtime()  # returns struct_time in UTC
        now = [raw.tm_year, raw.tm_mon, raw.tm_mday, raw.tm_hour, raw.tm_min, raw.tm_sec]
        return datetime.datetime(now,AC, anchor_date = anchor_date)
    #-----Support-Methods-------
    def finalize_full_datetime(self, value:list[int], epoch_type: str = AC, output_type="fulldatetime") -> datetime :
        """
        standart method meant to convert a list of values into a datetime object, considering their pre-set parameters
        """
        template_value_diccionary = {'y':0, 'm':1, 'd':1, 'h':0, 'mi':0, 's':0}
        for i in range(len(self.template)):
            for key in template_value_diccionary:
                if self.template[i] == key:
                    try:
                        template_value_diccionary[key] = value[i]
                        break
                    except IndexError:
                        break

        template_value_diccionary = self.normalize_full(template_value_diccionary)
        total_raw = self.convert_input_to_rawtime(template_value_diccionary)
        if epoch_type == BC:
            total_raw = -total_raw

        self.rawtime = total_raw
    
        parts = self.convert_rawtime_to_date(total_raw)



        self.output = [parts, output_type]
        datetime_support.__init__(self)
        return self   
    def value_template_extractor(self, value: str | list[float | int], template: str) -> list[int] | list[str]:
        """
        if the value or the template are normal strings, it converts them into lists while trying to find their values
        if the value is a list[float | int], it just sends it back, same if the template is a list[str]
        """

        # handle people accidentally using brackets [] to store the full str value
        if (isinstance(value, list) and all(isinstance(x, str) for x in value)):
            value = value[0]

        # detect value if str
        if isinstance(value, str):
            NUMS = set("0123456789.")
            one_number: str = ""
            several_numbers: list[float] = []

            for val in value:
                if val in NUMS:
                    one_number += val
                else:
                    if one_number.strip():
                        several_numbers.append(float(one_number))
                    one_number = ""

            if one_number and all(nm in NUMS for nm in one_number):
                several_numbers.append(float(one_number))

            value: list[float] = several_numbers

        # detect value if list[float | int]
        elif not all(isinstance(item, (float, int)) for item in value):
            # RAISE ISSUE
            pass

        # detect template if str
        if isinstance(template, str):
            template = template.lower()
            tmp = []
            for item in self.TIME_UNITS:
                if item in template:
                    tmp.append(item)
                    template.replace(item, "")
            template = tmp

        # detect template if list[str]
        elif not all(isinstance(item, str) for item in template):
            # RAISE ISSUE
            pass

        if not value or not template:
            # RAISE ISSUE
            pass

        return [value, template]
    def convert_input_to_rawtime(self, template_value_diccionary: dict[str, float]) -> float:
        """
        Convert Y/m/d h:i:s into raw seconds and add anchor. Uses exact calendar days (handles leap years)
        and assumes input dict fields may be floats. Relies on normalize_full producing integer Y,M,D,h,mi
        and float s (seconds).
        """

        def is_leap_year(y: int) -> bool:
            return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

        def days_since_epoch(Y: int, M: int, D: int) -> int:
            """
            Count days from year 0, month 1, day 1 up to Y/M/D (exclusive of the target day).
            Uses real month lengths and leap years. Returns an integer number of days.
            """
            mdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            days = 0

            # count full years
            for y in range(0, Y):
                days += 366 if is_leap_year(y) else 365

            # count full months in final year
            for m in range(1, M):
                if m == 2:
                    days += 29 if is_leap_year(Y) else 28
                else:
                    days += mdays[m - 1]

            # days in current month: D is 1-based, so D-1 full days have passed
            return days + (D - 1)

        vals = template_value_diccionary

        # normalize_full should have been applied upstream, but guard anyway:
        Y = int(vals.get("y", 1))
        M = int(vals.get("m", 1))
        D = int(vals.get("d", 1))
        h = int(vals.get("h", 0))
        i = int(vals.get("mi", 0))
        s = float(vals.get("s", 0))

        total_days = days_since_epoch(Y, M, D)
        total = total_days * 86400 + h * 3600 + i * 60 + s

        return float(total) + self.anchor
    def anchor_converter(self, anchor_date: datetime | float | int) -> float:
        """
        converts anchors into floats for more homogenous handling across methods
        """
        if isinstance(anchor_date, (float, int)):
            return float(anchor_date)
        elif isinstance(anchor_date, datetime):
            return anchor_date.rawtime
        else:
            # RAISE ISSUE
            pass
    def normalize_full(self, full: dict[str, float]) -> dict[str, float]:
        """
        Robust normalization that:
        - Accepts floats in any field
        - Carries fractional parts precisely by converting fractional years/months to days
        using the accurate length of the specific year/month in question
        - Carries seconds->minutes->hours->days (seconds kept as float)
        - Returns ints for Y,M,D,h,mi and float for s
        """

        # local helpers
        def is_leap_year(y: int) -> bool:
            return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

        def days_in_month(year: int, month: int) -> int:
            if month == 2:
                return 29 if is_leap_year(year) else 28
            return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]

        def days_in_year(year: int) -> int:
            return 366 if is_leap_year(year) else 365

        # read inputs as floats
        Yf = float(full.get("y", 0.0))
        Mf = float(full.get("m", 0.0))
        Df = float(full.get("d", 0.0))
        hf = float(full.get("h", 0.0))
        mif = float(full.get("mi", 0.0))
        sf = float(full.get("s", 0.0))

        # 1) Carry seconds -> minutes
        mif += int(sf // 60)
        sf = sf % 60.0

        # 2) Carry minutes -> hours
        hf += int(mif // 60)
        mif = mif % 60.0

        # 3) Carry hours -> days
        Df += int(hf // 24)
        hf = hf % 24.0

        # 4) Deal with fractional years
        Y_int = int(Yf)
        fracY = Yf - Y_int
        if fracY != 0.0:
            Df += fracY * days_in_year(Y_int)
        Y = Y_int

        # 5) Normalize months
        Mf_total = Mf
        M_int = int(Mf_total)
        fracM = Mf_total - M_int

        if M_int <= 0:
            M_int = 1

        years_from_months, M = divmod(M_int - 1, 12)
        M += 1
        Y += int(years_from_months)

        # 6) Fractional month -> convert to days
        if fracM != 0.0:
            Df += fracM * days_in_month(Y, M)

        # 7) Add leftover integer days
        D_whole = int(Df)
        D_frac = Df - D_whole
        day = D_whole

        # normalize day
        while True:
            dim = days_in_month(Y, M)
            if day < 1:
                M -= 1
                if M < 1:
                    M = 12
                    Y -= 1
                day += days_in_month(Y, M)
            elif day > dim:
                day -= dim
                M += 1
                if M > 12:
                    M = 1
                    Y += 1
            else:
                break

        # 8) Convert fractional day into h, mi, s
        hf += D_frac * 24.0
        h_int = int(hf)
        hf_frac = hf - h_int
        mif += hf_frac * 60.0
        mi_int = int(mif)
        mif_frac = mif - mi_int
        sf += mif_frac * 60.0

        # normalize seconds/minutes/hours
        mi_int += int(sf // 60)
        sf = sf % 60.0
        h_int += int(mi_int // 60)
        mi_int = mi_int % 60
        day += int(h_int // 24)
        h_int = h_int % 24

        # final day normalization
        while True:
            dim = days_in_month(Y, M)
            if day < 1:
                M -= 1
                if M < 1:
                    M = 12
                    Y -= 1
                day += days_in_month(Y, M)
            elif day > dim:
                day -= dim
                M += 1
                if M > 12:
                    M = 1
                    Y += 1
            else:
                break

        return {
            "y": int(Y if Y >= 1 else 1),
            "m": int(M if M >= 1 else 1),
            "d": int(day if day >= 1 else 1),
            "h": int(h_int),
            "mi": int(mi_int),
            "s": float(sf),
        }
    def convert_rawtime_to_date(self, seconds: float | int) -> list:
        """
        Convert rawtime into [Y, m, d, h, i, s], accounting for anchor.
        """

        def is_leap_year(y):
            return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

        days = int(seconds // 86400)
        rem = seconds % 86400
        Y = 0

        while True:
            year_days = 366 if is_leap_year(Y) else 365
            if days >= year_days:
                days -= year_days
                Y += 1
            else:
                break

        mdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        M = 1
        while True:
            dim = 29 if (M == 2 and is_leap_year(Y)) else mdays[M - 1]
            if days >= dim:
                days -= dim
                M += 1
            else:
                break

        D = days + 1
        h = int(rem // 3600)
        rem %= 3600
        i = int(rem // 60)
        s = rem % 60

        return [Y, M, D, h, i, float(s)]


a =datetime.datetime([2025,10,2])._object_only_accounts_for_.year

print(a)
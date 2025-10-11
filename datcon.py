from enum import Enum, auto
import time

# Define possible error types for the custom datetime system
class DatconErrorType(Enum):
    UNCORRECT_VALUE        = auto()
    TOO_MANY_PARAMETERS    = auto()
    UNCORRECT_INPUT_VALUE  = auto()
    F_IN_TEMPLATE          = auto()
    TOO_MANY_VALUES        = auto()
    UNREGISTERED_OPERATION = auto()
    UNKNOWN                = auto()


class DatconError(Exception):
    """
    Detailed exception for Datcon operations.

    Attributes:
        error_type   (DatconErrorType): kind of error
        place        (str): name of the method or step
        template     (Optional[str]): format template involved
        value        (Any): the offending input or intermediate value
        anchor_date  (Optional[float]): current ANCHOR_RAWTIME, if relevant
        critical     (bool): whether this should abort execution
    """
    __module__ = "builtins"
    def __init__(self,
                error_type: DatconErrorType,
                place: str,
                template: str = None,
                value: object = None,
                anchor_date: float = None,
                critical: bool = False):
        self.error_type  = error_type
        self.place       = place
        self.value       = value
        self.template    = template
        self.anchor_date = anchor_date
        self.critical    = critical

        # Build message components
        parts = [f" [{place}] {error_type.name.replace('_',' ').title()}"]

        if template is not None:
            parts.append(f"Template: {template!r}")

        if value is not None:
            parts.append(f"Value: {value!r}")

        if anchor_date is not None:
            parts.append(f"Anchor rawtime: {anchor_date}")

        # Add tailored hint
        hint = self._suggest_fix()
        if hint:
            parts.append(f"Hint: {hint}\n")

        msg = "\n" + " \n ".join(parts)
        super().__init__(msg)

    def _suggest_fix(self) -> str:
        # Provide specific hints for known cases
        if self.place == "intptime":
            if self.error_type is DatconErrorType.UNCORRECT_INPUT_VALUE:
                return "Ensure you passed a list of 6 numbers [Y,m,d,h,i,s]."
            if self.error_type in (DatconErrorType.TOO_MANY_VALUES,
                                DatconErrorType.TOO_MANY_PARAMETERS):
                return "Match the number of values to the template length."
        if self.place == "strptime":
            if self.error_type is DatconErrorType.UNCORRECT_INPUT_VALUE:
                return "Pass a string matching your template."
            if self.error_type in (DatconErrorType.TOO_MANY_VALUES,
                                DatconErrorType.TOO_MANY_PARAMETERS):
                return "Check that template tokens and digits in the string align."
        return "No hints available"

    def __str__(self):
        return self.args[0]


# Define possible calendar epochs
class EpochType(Enum):
    AC = "ac"  # After Christ (default)
    BC = "bc"  # Before Christ

    @property
    def epoch_offset(self) -> float:
        return 0.0

# Export enum for easier external use
AC = EpochType.AC
BC = EpochType.BC


class Datetime_support:
    # --- Extract only part of the datetime and compute rawtime accordingly ---

    def time(self):
        """Extract time (h:i:s) only and compute corresponding rawtime."""
        h, i, s = self.output[0][3:6]
        self.output = [[0,1,1,h,i,s], "time"]
        secs = h*3600 + i*60 + s
        self.rawtime = secs + self.epoch_type.epoch_offset
        print(self.output)
        return self

    def date(self):
        """Extract date (Y:m:d) only and compute rawtime."""
        Y, m, d = self.output[0][:3]
        self.output = [[Y,m,d,0,0,0], "date"]
        raw = convert_input_to_rawtime([Y,m,d,0,0,0], ['Y','m','d','h','i','s'])
        self.rawtime = raw + self.epoch_type.epoch_offset
        return self

    def year(self):
        """Extract year only and compute rawtime."""
        Y = self.output[0][0]
        self.output = [[Y,0,0,0,0,0], "year"]
        raw = convert_input_to_rawtime([Y,1,1,0,0,0], ['Y','m','d','h','i','s'])
        self.rawtime = raw + self.epoch_type.epoch_offset
        return self

    def month(self):
        """Extract month only and compute rawtime."""
        m = self.output[0][1]
        self.output = [[0,m,0,0,0,0], "month"]
        raw = convert_input_to_rawtime([0,m,1,0,0,0], ['Y','m','d','h','i','s'])
        self.rawtime = raw + self.epoch_type.epoch_offset
        return self

    def day(self):
        """Extract day only and compute rawtime."""
        d = self.output[0][2]
        self.output = [[0,1,d,0,0,0], "day"]
        raw = convert_input_to_rawtime([0,1,d,0,0,0], ['Y','m','d','h','i','s'])
        self.rawtime = raw + self.epoch_type.epoch_offset
        return self

    def hour(self):
        """Extract hour only and compute rawtime."""
        h = self.output[0][3]
        self.output = [[0,1,1,h,0,0], "hour"]
        raw = h*3600
        self.rawtime = raw + self.epoch_type.epoch_offset
        return self

    def minute(self):
        """Extract minute only and compute rawtime."""
        i = self.output[0][4]
        self.output = [[0,1,1,0,i,0], "minute"]
        raw = i*60
        self.rawtime = raw + self.epoch_type.epoch_offset
        return self

    def second(self):
        """Extract second only and compute rawtime."""
        s = self.output[0][5]
        self.output = [[0,1,1,0,0,s], "second"]
        raw = s
        self.rawtime = raw + self.epoch_type.epoch_offset
        return self

    def offset(self):
        """Reset datetime to just the epoch offset."""
        self.rawtime = self.epoch_type.epoch_offset
        self.output = ["fulldatetime", [0,0,0,0,0,0]]
        return self

    # Display methods (do not change rawtime)
    def time_show(self):
        """Change output type to 'time' for display."""
        return self.Parser("time")

    def date_show(self):
        """Change output type to 'date' for display."""
        return self.Parser("date")

    def year_show(self):
        return self.Parser("year")

    def month_show(self):
        return self.Parser("month")

    def day_show(self):
        return self.Parser("day")

    def hour_show(self):
        return self.Parser("hour")

    def minute_show(self):
        return self.Parser("minute")

    def second_show(self):
        return self.Parser("second")

    def Parser(self, type_swap):
        """Internal helper to set output type label."""
        pieces, _ = self.output
        self.output = [pieces, type_swap]
        return self

class Maths_Support:
    """
    Maths_Support provides arithmetic and comparison operations based on rawtime,
    enabling datetime objects to support intuitive math operations directly.

    These operations act upon the `rawtime` attribute, which represents time in seconds
    from a defined epoch.
    """
    def __init__(self, rawtime):
        self.rawtime = rawtime

    def __add__(self, other):
        """
        Add a scalar value (seconds) or another datetime's rawtime to this instance.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime + other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime + other)
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__add__"], True)

    def __sub__(self, other):
        """
        Subtract a scalar or another datetime's rawtime from this instance.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime - other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime - other)
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__sub__"], True)

    def __mul__(self, other):
        """
        Multiply this instance's rawtime with a scalar or another datetime's rawtime.
        Useful for scaling durations.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime * other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime * other)
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__mul__"], True)

    def __truediv__(self, other):
        """
        Perform true division of this instance's rawtime by a scalar or another rawtime.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime / other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime / other)
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__truediv__"], True)

    def __floordiv__(self, other):
        """
        Perform floor division on rawtime.
        Rounds down the result to the nearest integer.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime // other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime // other)
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__floordiv__"], True)

    def __mod__(self, other):
        """
        Return the remainder after dividing rawtime by scalar or another rawtime.
        Useful for measuring periodic cycles.
        Returns a float.
        """
        if isinstance(other, Maths_Support):
            return self.rawtime % other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime % other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__mod__"], True)

    def __pow__(self, other):
        """
        Raise rawtime to a given power (scalar or another rawtime).
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime ** other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime ** other)
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__pow__"], True)

    # Comparison operations return boolean values

    def __eq__(self, other):
        """Check equality between this instance and another rawtime or scalar."""
        if isinstance(other, Maths_Support):
            return self.rawtime == other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime == other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__eq__"], True)

    def __gt__(self, other):
        """Greater-than comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime > other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime > other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__gt__"], True)

    def __ge__(self, other):
        """Greater-than-or-equal-to comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime >= other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime >= other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__ge__"], True)

    def __lt__(self, other):
        """Less-than comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime < other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime < other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__lt__"], True)

    def __le__(self, other):
        """Less-than-or-equal-to comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime <= other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime <= other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__le__"], True)

    def __ne__(self, other):
        """Check inequality between this instance and another."""
        if isinstance(other, Maths_Support):
            return self.rawtime != other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime != other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__ne__"], True)

    def __repr__(self):
        """
        Prevent accidental use of __repr__ unless implemented explicitly.
        Triggers a DatconError to force conscious developer decisions.
        """
        other = None
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, None, [self, other], ["Maths_Support", "__repr__"], True)

class datetime:

    ANCHOR_RAWTIME = 0
    def __init__(self):
        self.time_units = {
            "Y": 31536000,
            "m": {
                1: 2678400, 2: 2419200, 3: 2678400, 4: 2592000,
                5: 2678400, 6: 2592000, 7: 2678400, 8: 2678400,
                9: 2592000, 10: 2678400, 11: 2592000, 12: 2678400},
            "d": 86400,
            "h": 3600,
            "i": 60,
            "s": 1,
        }
        self.rawtime = 0.0
        self.template = ['Y', 'm', 'd', 'h', 'i', 's']
        self.output = False
        self.epoch_type = AC

    def __str__(self):
        data, source = self.output
        Y, M, D, h, i, s = data
        sec = int(s) if float(s).is_integer() else s

        # Determine suffix and adjusted values based on calendar mode and rawtime
        suffix = ""
        display_Y = Y

        if self.epoch_type == AC:
            suffix = "A.C"
        elif self.epoch_type == BC:
            suffix = "B.C"


        # Format string based on source type
        if source == "fulldatetime":
            return f"({display_Y:04}-{M:02}-{D:02} {h:02}:{i:02}:{sec:02}) {suffix}"
        elif source == "date":
            return f"({display_Y:04}-{M:02}-{D:02}) {suffix}"
        elif source == "time":
            return f"({h:02}:{i:02}:{sec:02}) {suffix}"
        elif source == "year":
            return f"({display_Y:04}) {suffix}"
        elif source == "month":
            return f"({M:02}) {suffix}"
        elif source == "day":
            return f"({D:02}) {suffix}"
        elif source == "hour":
            return f"({h:02}) {suffix}"
        elif source == "minute":
            return f"({i:02}) {suffix}"
        elif source == "second":
            return f"({sec:02}) {suffix}"
        else:
            return "No source Found"



    @classmethod
    def stamp(cls, value, template: str, epoch_type: str = AC, anchor_date=0):
        cls.ANCHOR_RAWTIME = Calendar_converter(anchor_date)
        self = cls()
        self.epoch_type = epoch_type

        corrector = {"y": "Y", "D": "d", "H": "h", "S": "s"}
        parameters = []

        # If the value is a string → strptime branch
        if isinstance(value, str):
            NUMS = set("0123456789.")
            for ch in template:
                if ch not in ("%", "f"):
                    u = corrector.get(ch, ch)
                    if u in self.time_units and u not in parameters:
                        parameters.append(u)

            vals = []
            buf = ""
            for ch in value:
                if ch in NUMS:
                    buf += ch
                else:
                    if buf:
                        vals.append(float(buf))
                        buf = ""
            if buf:
                vals.append(float(buf))

            if len(vals) != len(parameters):
                err = (
                    DatconErrorType.TOO_MANY_PARAMETERS
                    if len(vals) < len(parameters)
                    else DatconErrorType.TOO_MANY_VALUES
                )
                raise DatconError(err, "stamp", template, vals, self.ANCHOR_RAWTIME, True)

            return self.finalize_full_datetime(vals, parameters, self.epoch_type, "fulldatetime")

        # If the value is a list/tuple of ints/floats → intptime branch
        elif isinstance(value, (list, tuple)) and all(isinstance(item, (int, float)) for item in value):
            for ch in template:
                u = corrector.get(ch, ch)
                if u in cls().time_units and u not in parameters:
                    parameters.append(u)

            if len(value) != len(parameters):
                err = (
                    DatconErrorType.TOO_MANY_PARAMETERS
                    if len(value) < len(parameters)
                    else DatconErrorType.TOO_MANY_VALUES
                )
                raise DatconError(err, "stamp", template, value, self.ANCHOR_RAWTIME, True)

            return self.finalize_full_datetime(value, parameters, self.epoch_type)

        else:
            raise DatconError([
                DatconErrorType.UNCORRECT_INPUT_VALUE,
                template, value,
                ["stamp", "unsupported_type"],
                True
            ])

    @classmethod
    def strptime(cls, input_value: str, template: str, epoch_type: str = AC, anchor_date: "datetime" = 0):
        """
        Parse a string according to `template` (e.g. "YmdHis") into a datetime.
        """

        cls.ANCHOR_RAWTIME = Calendar_converter(anchor_date )
        
        
        self = cls()
        self.epoch_type = epoch_type

        if not isinstance(input_value, str):
            raise DatconError([
                DatconErrorType.UNCORRECT_INPUT_VALUE,
                template, input_value,
                ["strptime", "input_value_wasnt_str"],
                True
            ])

        # Build the list of units to extract
        parameters = []
        corrector = {"y": "Y", "D": "d", "H": "h", "S": "s"}
        for ch in template:
            if ch not in ("%", "f"):
                u = corrector.get(ch, ch)
                if u in self.time_units and u not in parameters:
                    parameters.append(u)

        # Extract numeric substrings
        NUMS = set("0123456789.")
        vals = []
        buf = ""
        for ch in input_value:
            if ch in NUMS:
                buf += ch
            else:
                if buf:
                    vals.append(float(buf))
                    buf = ""
        if buf:
            vals.append(float(buf))
        
        # Ensure counts match
        if len(vals) != len(parameters):
            err = (
                DatconErrorType.TOO_MANY_PARAMETERS
                if len(vals) < len(parameters)
                else DatconErrorType.TOO_MANY_VALUES
            )
            raise DatconError(err,"strptime",template,vals,self.ANCHOR_RAWTIME,True)

        # Finalize and return
        return self.finalize_full_datetime(vals, parameters, self.epoch_type, "fulldatetime", )
    @classmethod
    def intptime(cls, value: list[int], template: str, epoch_type: str = AC, anchor_date=0):
        self = cls()
        cls.ANCHOR_RAWTIME = Calendar_converter(anchor_date)
        self.epoch_type = epoch_type

        # 1) Validate that every item in value is numeric
        for item in value:
            if not isinstance(item, (int, float)):
                err = DatconErrorType.UNCORRECT_INPUT_VALUE
                raise DatconError(err,"intptime",template,value,self.ANCHOR_RAWTIME,True)

        # 2) Build the list of expected parameters using the same corrector logic as strptime
        corrector = {"y": "Y", "D": "d", "H": "h", "S": "s"}
        parameters = []
        for ch in template:
            u = corrector.get(ch, ch)
            if u in cls().time_units and u not in parameters:
                parameters.append(u)

        # 3) Now ensure the counts match
        if len(value) != len(parameters):
            err = (
                DatconErrorType.TOO_MANY_PARAMETERS
                if len(value) < len(parameters)
                else DatconErrorType.TOO_MANY_VALUES
            )
            raise DatconError(err, "intptime",template,value,self.ANCHOR_RAWTIME,True)

        # 4) Finally, hand off to your normal finalizer
        return self.finalize_full_datetime(value, parameters, self.epoch_type)
    @classmethod
    def operand(cls,offset_seconds: float,reverse: bool = False,anchor_date=0):

        """
        Treat `offset_seconds` as seconds *after* year‑0, then subtract
        the anchor’s rawtime so that `rawtime = anchor – offset_seconds`.
        If `reverse=True`, flips the sign of `offset_seconds` first.
        """
        # 1) Convert anchor_date → raw seconds base
        base = Calendar_converter(anchor_date)

        # 2) Apply reverse flag to offset if needed
        if reverse:
            offset_seconds = -offset_seconds

        # 3) Compute the “true” rawtime = anchor – offset
        absolute = base - offset_seconds

        # 4) Decide era and magnitude for display
        if absolute < 0:
            era = BC
            secs = -absolute
        else:
            era = AC
            secs = absolute

        # 5) For printing, set ANCHOR_RAWTIME = base so convert_rawtime_to_date
        #    adds the anchor back; then restore the old anchor.
        old_anchor = cls.ANCHOR_RAWTIME
        cls.ANCHOR_RAWTIME = base
        parts = convert_rawtime_to_date(secs)
        cls.ANCHOR_RAWTIME = old_anchor

        # 6) Build and return the datetime instance
        inst = cls()
        inst.epoch_type = era
        inst.rawtime    = absolute
        inst.output     = [parts, "fulldatetime"]
        return inst
    @classmethod
    def datetime(cls, value: list[int], epoch_type: str = AC, anchor_date=0):
        self = cls()
        cls.ANCHOR_RAWTIME = Calendar_converter(anchor_date)
        self.epoch_type = epoch_type
        return self.finalize_full_datetime(value, self.template, self.epoch_type)
    @classmethod
    def timedate(cls, value: list, epoch_type: str = AC, anchor_date=0):
        self = cls()
        cls.ANCHOR_RAWTIME = Calendar_converter(anchor_date)
        self.epoch_type = epoch_type
        rev_tmpl = list(reversed(self.template))
        return self.finalize_full_datetime(value, rev_tmpl, self.epoch_type)
    @classmethod
    def current_time(cls, anchor_date=0):
        """
        Returns the current real-world UTC time as [Y, m, d, h, i, s],
        without using the `datetime` module.
        """
        raw = time.gmtime()  # returns struct_time in UTC
        now = [raw.tm_year, raw.tm_mon, raw.tm_mday, raw.tm_hour, raw.tm_min, raw.tm_sec]
        return datetime.datetime(now,AC, anchor_date)
    def finalize_full_datetime(self, value, parameters: str, epoch_type: str, output_type="fulldatetime"):
        self.epoch_type = epoch_type

        template_lower = [key.lower() for key in self.template]
        parameters_lower = [param.lower() for param in parameters]
        param_value_map = dict(zip(parameters_lower, value))

        # Fill in defaults
        full = []
        for key in template_lower:
            if key in param_value_map:
                full.append(param_value_map[key])
            else:
                full.append(1 if key in ('m', 'd') else 0)

        full = normalize_full(full)

        # Convert to rawtime and apply anchor
        total_raw = convert_input_to_rawtime(full, self.template)
        if epoch_type == BC:
            total_raw = -total_raw

        self.rawtime = total_raw
        parts = convert_rawtime_to_date(total_raw)
        self.output = [parts, output_type]
        return self     
def convert_input_to_rawtime(value: list, parameters: list, hour_difference=0) -> float:
    """Convert Y/m/d h:i:s into raw seconds and subtract anchor."""
    
    def is_leap_year(y):
        return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

    def days_since_epoch(Y, M, D):
        mdays = [31,28,31,30,31,30,31,31,30,31,30,31]
        days = 0
        ref_year = 0
        for y in range(ref_year, Y):
            days += 366 if is_leap_year(y) else 365
        for m in range(1, M):
            days += 29 if (m == 2 and is_leap_year(Y)) else mdays[m-1]
        return days + (D - 1)

    vals = dict(zip(parameters, value))
    Y = int(vals.get('Y', 0))
    M = int(vals.get('m', 0))
    D = int(vals.get('d', 0))
    h = int(vals.get('h', 0))
    i = int(vals.get('i', 0))
    s = float(vals.get('s', 0))

    total = days_since_epoch(Y, M, D) * 86400 + h * 3600 + i * 60 + s + hour_difference * 3600

    return float(total) - datetime.ANCHOR_RAWTIME
def convert_rawtime_to_date(seconds: int | float) -> list:
    """Convert rawtime into [Y, m, d, h, i, s], accounting for anchor."""

    def is_leap_year(y):
        return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

    seconds += datetime.ANCHOR_RAWTIME
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

    mdays = [31,28,31,30,31,30,31,31,30,31,30,31]
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
def normalize_full(full: list[int]) -> list[int]:
    """
    Normalize a full [Y, M, D, h, i, s] list:
    - Carries overflow from seconds → minutes → hours → days
    - Adjusts months > 12 or < 1
    - Converts overlarge day values into correct month/year
    - Handles leap years and month lengths
    """

    Y, M, D, h, i, s = full

    # Carry seconds → minutes
    i += s // 60
    s = s % 60

    # Carry minutes → hours
    h += i // 60
    i = i % 60

    # Carry hours → days
    D += h // 24
    h = h % 24

    # Normalize month (make sure 1 <= M <= 12)
    if M < 1 or M > 12:
        years_delta, M = divmod(M - 1, 12)
        M += 1
        Y += years_delta

    # Helper: days in a given month
    def days_in_month(year, month):
        if month == 2:
            # Leap year check
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            return 28
        return [31,28,31,30,31,30,31,31,30,31,30,31][int(month) - 1]

    # Carry days → months (may loop multiple months)
    while True:
        dim = days_in_month(Y, M)
        if D < 1:
            # Borrow from previous month
            M -= 1
            if M < 1:
                M = 12
                Y -= 1
            D += days_in_month(Y, M)
        elif D > dim:
            D -= dim
            M += 1
            if M > 12:
                M = 1
                Y += 1
        else:
            break

    return [Y, M, D, h, i, s]
def Calendar_converter(anchor: datetime | float | int = 0) -> float:
    """
    Convert a datetime instance, raw float seconds, or integer year into rawtime.
    """
    if isinstance(anchor, (int, float)):
        return float(anchor)
    elif isinstance(anchor, datetime):
        return float(anchor.rawtime)
    return 0.0

__all__ = [
    "DatconErrorType",
    "DatconError",
    "EpochType",
    "AC",
    "BC",
    "Datetime_support",
    "Maths_Support",
    "datetime",
    "convert_input_to_rawtime",
    "convert_rawtime_to_date",
    "normalize_full",
    "Calendar_converter"
]
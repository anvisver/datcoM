from enum import Enum, auto
import time

# Define possible error types for the custom datetime system
class DatconErrorType(Enum):
    """
    contains the Error-types ussed in DatconError to handle issues in this datetime package\n
    
    INCORRECT_VALUE\n    
    TOO_MANY_PARAMETERS\n    
    TOO_MANY_VALUES\n  
    UNREGISTERED_OPERATION\n
    UNKNOWN\n             
    INCORRECT_ANCHOR_VALUE\n 
    
    """

    INCORRECT_VALUE        = auto()
    TOO_MANY_PARAMETERS    = auto()
    TOO_MANY_VALUES        = auto()
    UNREGISTERED_OPERATION = auto()
    UNKNOWN                = auto()
    INCORRECT_ANCHOR_VALUE = auto()

class DatconError(Exception):
    """
    DatconError: enriched exception with actionable hints.

    Constructor signature remains:
        DatconError(error_type, place, template=None, value=None, anchor_date=None, critical=False)

    - error_type: DatconErrorType enum
    - place: str or list indicating function/module and subcomponent
    - template: optional template string involved
    - value: the offending value(s)
    - anchor_date: optional anchor seconds (for anchor-related errors)
    - critical: whether this is considered fatal
    """
    def __init__(self, error_type:str, place:str, template: str = None, value:list[int] | str =None, anchor_date: float | int =None, critical: bool = False):
        self.error_type = error_type
        self.place = place
        self.template = template
        self.value = value
        self.anchor_date = anchor_date
        self.critical = bool(critical)
        msg = self._build_message()
        super().__init__(msg)

    def _build_message(self) -> str:
        parts = []
        parts.append(f"{self.error_type.name}: occurred in {self.place!r}")
        if self.template is not None:
            parts.append(f"Template: {self.template!r}")
        if self.value is not None:
            parts.append(f"Value: {self.value!r}")
        if self.anchor_date is not None:
            parts.append(f"Anchor (seconds): {self.anchor_date!r}")
        parts.append(f"Critical: {self.critical}")
        hint = self._suggest_fix()
        if hint:
            parts.append("Suggestion: " + hint)
        return "\n".join(parts)

    def _suggest_fix(self) -> str:
        et = self.error_type
        p = self.place
        if et.name == 'INCORRECT_ANCHOR_VALUE':
            return ("Anchor value is not recognised. Pass a float (raw seconds), a datetime-like object, "
                    "or an integer year (e.g. 2000). If you passed a small int and intended seconds, use a float (7200.0).")
        if et.name == 'INCORRECT_VALUE':
            if isinstance(p, (list, tuple)) and len(p) >= 1 and p[0] == 'stamp':
                return "Stamp input format mismatch. Ensure a list of 6 numbers [Y,m,d,h,i,s] or a matching template string."
            return "Check the value(s) supplied to the function; types or ranges may be invalid."
        if et.name == 'TOO_MANY_PARAMETERS' or et.name == 'TOO_MANY_VALUES':
            return "Too many parameters/values for the given template. Make sure the number of tokens matches the number of values."
        if et.name == 'UNREGISTERED_OPERATION':
            return "Operation between provided operand types is not supported. Convert operands to compatible types or implement the operation."
        if isinstance(p, str) and 'Calendar' in p:
            return "Check anchor conversion code: Calendar_converter should return seconds to ADD (not apply class anchor twice)."
        if isinstance(p, (list, tuple)) and 'int' in p:
            return "Integer inputs may be ambiguous (year vs seconds). Prefer explicit types: use datetime objects or floats for seconds."
        return None




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

CENTRAL_EUROPEAN_TIMELINE = float(7200)

class Datetime_support:
    # --- Extract only part of the datetime and compute rawtime accordingly ---

    def time(self):
        """Extract time (h:i:s) only and compute corresponding rawtime."""
        h, i, s = self.output[0][3:6]
        self.output = [[0,1,1,h,i,s], "time"]
        secs = h*3600 + i*60 + s
        self.rawtime = secs + self.epoch_type.epoch_offset
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
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__add__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)

    def __sub__(self, other):
        """
        Subtract a scalar or another datetime's rawtime from this instance.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime - other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime - other)
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__sub__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)


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
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__mul__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)

    def __truediv__(self, other):
        """
        Perform true division of this instance's rawtime by a scalar or another rawtime.
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime / other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime / other)
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__truediv__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)


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
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__floordiv__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)


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
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__mod__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)


    def __pow__(self, other):
        """
        Raise rawtime to a given power (scalar or another rawtime).
        Returns a new datetime object.
        """
        if isinstance(other, Maths_Support):
            return datetime.operand(self.rawtime ** other.rawtime)
        elif isinstance(other, (int, float)):
            return datetime.operand(self.rawtime ** other)
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__pow__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)


    # Comparison operations return boolean values

    def __eq__(self, other):
        """Check equality between this instance and another rawtime or scalar."""
        if isinstance(other, Maths_Support):
            return self.rawtime == other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime == other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__eq__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)

    def __gt__(self, other):
        """Greater-than comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime > other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime > other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__gt__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)


    def __ge__(self, other):
        """Greater-than-or-equal-to comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime >= other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime >= other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__ge__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)


    def __lt__(self, other):
        """Less-than comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime < other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime < other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__lt__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)


    def __le__(self, other):
        """Less-than-or-equal-to comparison."""
        if isinstance(other, Maths_Support):
            return self.rawtime <= other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime <= other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__le__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)


    def __ne__(self, other):
        """Check inequality between this instance and another."""
        if isinstance(other, Maths_Support):
            return self.rawtime != other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime != other
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__ne__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)


    def __repr__(self):
        """
        Prevent accidental use of __repr__ unless implemented explicitly.
        Triggers a DatconError to force conscious developer decisions.
        """
        other = None
        raise DatconError(DatconErrorType.UNREGISTERED_OPERATION, ["Maths_Support", "__repr__"],[self.template,other.template], [self.rawtime, other.rawtime],[self.template,other.template] , True)

class datetime(Maths_Support,Datetime_support):
    """
    Welcome to the **Custom Datetime System**!

    This project is a complete, hand-crafted alternative to Python’s built-in `datetime` module. It provides full support for creating, manipulating, and displaying dates and times without depending on any external libraries. Instead of relying on complex built-in types, this system represents every moment as a single number called **`rawtime`**, which is the total number of seconds counted from a chosen starting point (the epoch). From this internal representation, all dates and times can be built, displayed, and calculated.

    ---

    ## How It Works
    At its core, the system converts any date or time into `rawtime`. You can think of `rawtime` as a timeline measured only in seconds. Once a moment is stored in this format, the system can:
    - Convert it back into years, months, days, hours, minutes, and seconds.
    - Perform arithmetic (e.g., add or subtract seconds, days, years).
    - Compare two dates to see which one is earlier or later.

    ---

    ## Main Components

    ### 1. `datetime` (Main Class)
    The `datetime` class is the centerpiece of the system. It provides a wide range of tools:
    - **Creation**: Build datetime objects from strings, lists of numbers, or numeric values.
    - **Display**: Show a datetime in a clean, human-readable format.
    - **Arithmetic**: Add or subtract values like seconds, minutes, or days.
    - **Comparison**: Check if one date is earlier or later than another.
    - **Conversion**: Switch between human-readable parts and the internal `rawtime`.

    Key functions include:
    - `datetime.stamp()`: Create a datetime from a string, list, or template.
    - `datetime.current_time()`: Get the current UTC time as a datetime.
    - `datetime.operand()`: Build a datetime from an offset of seconds relative to an anchor.
    - `datetime.show()`: Display the object as a formatted string.

    ### 2. Support Classes
    - **`Datetime_support`**: Provides functions to extract or focus on only the *date* (year, month, day) or only the *time* (hours, minutes, seconds).
    - **`Maths_Support`**: Supplies arithmetic and comparison operators. With it, you can:
    - Add numbers to a datetime (e.g., `dt + 86400` → one day later).
    - Subtract one datetime from another.
    - Compare datetimes with `<`, `>`, `==`, etc.

    ### 3. Error Handling (`DatconError`)
    Mistakes are explained with a custom exception called `DatconError`. Instead of a generic error, this system gives:
    - A description of what went wrong.
    - The type of error (such as `INCORRECT_VALUE` or `UNREGISTERED_OPERATION`).
    - Helpful hints for fixing the mistake (like checking if the input format matches the template).

    ### 4. Epoch Types
    The system supports both **AC** (After Christ) and **BC** (Before Christ) eras. Dates can move forward or backward in time, and the system will adjust the internal `rawtime` value accordingly.

    ---

    ## Features in Detail

    ### Creating Datetime Objects
    You can create objects in several ways:
    ```python
    # From a string and a template
    d = datetime.stamp("2025-09-19 12:34:56", template="%Y-%m-%d %H:%i:%s")

    # From a list of numbers
    d2 = datetime.stamp([2025, 9, 19, 12, 34, 56])

    # From the current system time
    now = datetime.current_time()
    ```

    ### Performing Arithmetic
    Datetimes can be modified with standard math operations:
    ```python
    # Add one hour to a datetime
    d_plus_hour = d + 3600

    # Subtract two datetimes (gives a difference)
    diff = d2 - d

    # Multiply or divide rawtime values
    d_scaled = d * 2
    ```

    ### Comparing Dates
    You can compare datetime objects directly:
    ```python
    if d2 > d:
        print("d2 comes after d")
    ```

    ### Displaying Results
    Printing a datetime gives you a human-friendly representation:
    ```python
    print(d)   # (2025-09-19 12:34:56) A.C
    print(now) # (2025-09-19 14:07:03) A.C (for example)
    ```

    ---

    ## How the System Calculates Dates
    - **Internal representation**: Everything is stored in seconds (`rawtime`).
    - **Conversion to date parts**: A built-in function converts `rawtime` into year, month, day, hour, minute, and second.
    - **Leap years**: The system correctly accounts for leap years when handling February.
    - **Months**: Each month has its proper length (28–31 days).
    - **Anchors**: An anchor defines the starting point for calculations. By default, a European timeline constant is used, but you can set your own.

    ---

    ## Example Workflow
    ```python
    # Step 1: Create a datetime from a string
    d1 = datetime.stamp("2025-09-19 12:00:00", template="%Y-%m-%d %H:%i:%s")

    # Step 2: Add some time
    one_day_later = d1 + 86400  # add one day

    # Step 3: Compare with another datetime
    d2 = datetime.stamp([2025, 9, 20, 12, 0, 0])
    print(d2 == one_day_later)  # True

    # Step 4: Print results
    print(d1)            # (2025-09-19 12:00:00) A.C
    print(one_day_later) # (2025-09-20 12:00:00) A.C
    ```

    ---

    ## Why Use This System?
    - **Independence**: Works without Python’s built-in `datetime`.
    - **Flexibility**: Accepts many input forms (strings, numbers, lists).
    - **Clarity**: Outputs are simple and easy to read.
    - **Control**: You can work directly with raw seconds if you want low-level precision.

    ---

    This system provides all the tools needed to manage time, from simple tasks like printing today’s date to advanced operations like handling eras, anchors, and detailed arithmetic. It is designed to be approachable for beginners but powerful enough for advanced use.
    """
    ANCHOR_RAWTIME:float = 0
    def __init__(self) -> "datetime":
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
    def __str__(self) -> "datetime":
        data, source = self.output
        Y, M, D, h, i, s = data
        sec = int(s) if float(s).is_integer() else float(s)

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
    def stamp(cls, value: list[int] | str = [0,1,1,0,0,0], template: list[str] | str = ['Y', 'm', 'd', 'h', 'i', 's'], epoch_type: EpochType = AC, anchor_date: float | int = 0) -> "datetime":
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
                raise DatconError(err, ["stamp", "str"], template, vals, self.ANCHOR_RAWTIME, True)

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
                raise DatconError(error_type=DatconErrorType.INCORRECT_VALUE,
                  place=["stamp","int"],
                  template=parameters,
                  value=value,
                  anchor_date=None,
                  critical=True)

            return self.finalize_full_datetime(value, parameters, self.epoch_type, "fulldatetime")

        else:
            raise DatconError(
                DatconErrorType.INCORRECT_VALUE,
                ["stamp", "unsupported_type"],
                template, value, self.ANCHOR_RAWTIME,
                True)
    @classmethod
    def operand(cls,offset_seconds: float | int,reverse: bool = False,anchor_date: float | int = 0) -> "datetime":
        """
        Treat `offset_seconds` as seconds *after* year‑0, then subtract
        the anchor’s rawtime so that `rawtime = anchor – offset_seconds`.
        If `reverse=True`, flips the sign of `offset_seconds` first.
        """
        if isinstance(offset_seconds,datetime):
            offset_seconds = offset_seconds.rawtime
        # 1) Convert anchor_date → raw seconds base
        base = Calendar_converter(anchor_date)

        # 2) Apply reverse flag to offset if needed
        if reverse:
            offset_seconds = -offset_seconds

        # 3) Compute the “true” rawtime = anchor – offset
        absolute = offset_seconds - base

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
    def datetime(cls, value: list[int] | str = "0", epoch_type: EpochType = AC, anchor_date: float | int = 0) -> "datetime":
        self = cls()
        parameters = []

        if isinstance(value, str):

            vals = []
            buf = ""
            NUMS = set("0123456789.")

            traceback = True
            for ch in value:
                if ch in NUMS:
                    buf += ch
                    traceback = False
                else:
                    if buf:
                        vals.append(float(buf))
                        buf = ""
            if buf:
                vals.append(float(buf))
            
            if traceback:
                vals = [0]

            for i in range(len(vals)):
                if i<(len(self.template)):
                    parameters.append(self.template[i])
                else:
                    err = DatconErrorType.TOO_MANY_VALUES
                    raise DatconError(err, ["datetime", "str"], self.template, vals, self.ANCHOR_RAWTIME, True)

            return self.finalize_full_datetime(vals, parameters, self.epoch_type)
        elif isinstance(value, (list, tuple)) and all(isinstance(item, (int, float)) for item in value):
            if len(value) < 1:
                value = [0]
            cls.ANCHOR_RAWTIME = Calendar_converter(anchor_date)
            self.epoch_type = epoch_type
            return self.finalize_full_datetime(value, self.template, self.epoch_type)
        else:
            err = DatconErrorType.INCORRECT_VALUE
            raise DatconError(err, ["datetime"], self.template, vals, self.ANCHOR_RAWTIME, True)
    @classmethod
    def timedate(cls, value: list[int] | str = "0", epoch_type: EpochType = AC, anchor_date: float | int = 0) -> "datetime":
        self = cls()
        parameters = []
        template = list(reversed(self.template))
        if isinstance(value, str):

            vals = []
            buf = ""
            NUMS = set("0123456789.")

            traceback = True
            for ch in value:
                if ch in NUMS:
                    buf += ch
                    traceback = False
                else:
                    if buf:
                        vals.append(float(buf))
                        buf = ""
            if buf:
                vals.append(float(buf))
            
            if traceback:
                vals = [0]

            for i in range(len(vals)):
                if i<(len(template)):
                    parameters.append(template[i])
                else:
                    err = DatconErrorType.TOO_MANY_VALUES
                    raise DatconError(err, ["timedate", "str"],template, vals, self.ANCHOR_RAWTIME, True)

            return self.finalize_full_datetime(vals, parameters, self.epoch_type, "fulldatetime")
        elif isinstance(value, (list, tuple)) and all(isinstance(item, (int, float)) for item in value):
            if len(value) < 1:
                value = [0]
            cls.ANCHOR_RAWTIME = Calendar_converter(anchor_date)
            self.epoch_type = epoch_type
            return self.finalize_full_datetime(value, template, self.epoch_type)
        else:
            err = DatconErrorType.INCORRECT_VALUE
            raise DatconError(err, ["timedate"], template, vals, self.ANCHOR_RAWTIME, True)
    @classmethod
    def current_time(cls, anchor_date: float | int = CENTRAL_EUROPEAN_TIMELINE) -> "datetime":
        """
        Returns the current real-world UTC time as [Y, m, d, h, i, s],
        without using the `datetime` module.
        """
        raw = time.gmtime()  # returns struct_time in UTC
        now = [raw.tm_year, raw.tm_mon, raw.tm_mday, raw.tm_hour, raw.tm_min, raw.tm_sec]
        return datetime.datetime(now,AC, anchor_date)
    def show(self) -> "datetime":
        return datetime.operand(self.rawtime)  
    def finalize_full_datetime(self, value, parameters: str, epoch_type: str, output_type="fulldatetime") -> "datetime":
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
def convert_input_to_rawtime(value: list[int], parameters: list) -> float:
    """Convert Y/m/d h:i:s into raw seconds and adds anchor."""
    
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

    total = days_since_epoch(Y, M, D) * 86400 + h * 3600 + i * 60 + s 

    return float(total) + datetime.ANCHOR_RAWTIME
def convert_rawtime_to_date(seconds: float | int) -> list:
    """Convert rawtime into [Y, m, d, h, i, s], accounting for anchor."""

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
    raise DatconError(error_type = DatconErrorType.INCORRECT_ANCHOR_VALUE, place = "Calendar_converter", anchor_date = anchor,critical = True  )

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
















a = datetime.current_time()

print(a)


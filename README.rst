===========
TimeConvert
===========

TimeConvert is a simple time convert script(library) for Python, built for human beings.

Installation
============

::

    pip install TimeConvert


Usage
=====

::

    from TimeConvert import TimeConvert as tc

    tc.utc_timestamp()


Comparison
==========
::

+------------------+------------------------------+--------------+
| Function Points  | TimeConvert                  | Other        |
+==================+==============================+==============+
| TimeStamp        | tc.local_timestamp(ms=True)  | time.time()  |
+------------------+------------------------------+--------------+


Variable
========

::

    # Default Asia/Shanghai & %Y-%m-%d %H:%M:%S
    from TimeConvert import TIME_ZONE, TIME_FORMAT

    # Deassign TIME_ZONE & TIME_FORMAT
    tc.__init__(timezone='Asia/Shanghai', format='%Y-%m-%d %H:%M:%S')


Method
======

::

    # VALIDATE

    def validate_string(self, string, format=None):

    # REPLACE

    def remove_microsecond(self, self, dt):

    # DATETIME

    def utc_datetime(self, dt=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):

    def local_datetime(self, dt=None, utc=False, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):

    def is_utc_datetime(self, dt):

    def is_local_datetime(self, dt, local_tz=None):

    def to_utc_datetime(self, dt, timezone=None):

    def to_local_datetime(self, dt, timezone=None):

    def yesterday_utc_datetime(self, ms=True):

    def tomorrow_utc_datetime(self, ms=True):

    def yesterday_local_datetime(self, ms=True, timezone=None):

    def tomorrow_local_datetime(self, ms=True, timezone=None):

    def several_days_ago(self, dt=None, utc=True, timezone=None, days=0):

    def several_days_coming(self, dt=None, utc=True, timezone=None, days=0):

    def several_time_ago(self, dt=None, utc=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):

    def several_time_coming(self, dt=None, utc=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):

    # DATE

    def utc_date(self, dt: Optional[datetime.datetime] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> datetime.date:

    def local_date(self, dt: Optional[datetime.datetime] = None, utc: bool = False, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> datetime.date:

    def datetime_to_date(self, dt: datetime.datetime) -> datetime.date:

    def to_date(self, value: Union[str, datetime.datetime, datetime.date], format: Optional[str] = None, idx: int = 0) -> Optional[datetime.date]:

    def is_the_same_day(self, dt1: datetime.date, dt2: datetime.date) -> bool:

    # WEEK

    def utc_week(self, dt: Optional[datetime.datetime] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False, mode: int = 3) -> str:

    def local_week(self, dt: Optional[datetime.datetime] = None, utc: bool = False, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False, mode: int = 3) -> str:

    def to_week(self, value: Union[str, datetime.datetime, datetime.date], format: Optional[str] = None, idx: int = 0) -> Optional[Week]:

    # STRING

    # DATETIME_STRING
    def datetime_to_unicode_string(self, dt, format=None):

    def datetime_to_string(self, dt, format=None, isuc=False):

    def yesterday_utc_string(self, format=None, ms=True, isuc=False):

    def tomorrow_utc_string(self, format=None, ms=True, isuc=False):

    def yesterday_local_string(self, format=None, ms=True, timezone=None, isuc=False):

    def tomorrow_local_string(self, format=None, ms=True, timezone=None, isuc=False):

    def several_days_ago_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, days=0, isuc=False):

    def several_days_coming_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, days=0, isuc=False):

    def several_time_ago_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, isuc=False):

    def several_time_coming_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, isuc=False):

    def utc_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, local_dt=None, utc_dt=None, isuc=False):

    def local_string(self, dt=None, format=None, utc=False, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, local_dt=None, utc_dt=None, isuc=False):

    def utc_datetime_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, local_dt=None, utc_dt=None, isuc=False):

    def local_datetime_string(self, dt=None, format=None, utc=False, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, local_dt=None, utc_dt=None, isuc=False):

    # DATE_STRING
    def utc_date_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, local_dt=None, utc_dt=None, isuc=False):

    def local_date_string(self, dt=None, format=None, utc=False, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, local_dt=None, utc_dt=None, isuc=False):

    # WEEK_STRING
    def utc_week_string(self, dt: Optional[datetime.datetime] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False, mode: int = 3) -> str:

    def local_week_string(self, dt: Optional[datetime.datetime] = None, utc: bool = False, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False, mode: int = 3) -> str:

    # TIMESTAMP

    def utc_timestamp(self, utc_dt=None, ms=False, micro=False, milli=False, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):

    def local_timestamp(self, local_dt=None, ms=False, micro=False, milli=False, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):

    def datetime_to_timestamp(self, dt, ms=False):

    def structime_to_timestamp(self, structime):

    def seconds_to_microseconds(self, s):

    def seconds_to_milliseconds(self, s):

    # STRING ==> DATE

    def string_to_date(self, string, format=None):

    def string_to_utc_date(self, string, format=None):

    def string_to_local_date(self, string, format=None):

    def utc_string_to_utc_date(self, utc_string, format=None):

    def utc_string_to_local_date(self, utc_string, format=None):

    # STRING ==> DATETIME

    def string_to_datetime(self, string, format=None):

    def string_to_utc_datetime(self, string, format=None):

    def string_to_local_datetime(self, string, format=None):

    def utc_string_to_utc_datetime(self, utc_string, format=None):

    def utc_string_to_local_datetime(self, utc_string, format=None):

    # STRING ==> TIMESTAMP

    def string_to_timestamp(self, string, format=None, ms=False):

    def string_to_utc_timestamp(self, string, format=None, ms=False):

    def string_to_local_timestamp(self, string, format=None, ms=False):

    # TIMESTAMP ==> DATETIME

    def timestamp_to_datetime(self, stamp):

    def timestamp_to_utc_datetime(self, stamp):

    def timestamp_to_local_datetime(self, stamp):

    def utc_timestamp_to_utc_datetime(self, stamp):

    def utc_timestamp_to_local_datetime(self, stamp):

    # TIMESTAMP ==> AGE

    # TIME_DELTA

    def timestamp_delta(self, stamp1, stamp2, interval=None):

    def datetime_delta(self, dt1, dt2, interval=None):

    def string_delta(self, string1, string2, interval=None, format=None, format1=None, format2=None):

    PS: interval(seconds) —— Time1 - Time2 >= interval ?

    # TIME_COUNT_DOWN

    def timestamp_countdown(self, stamp, utc=True):

    def datetime_countdown(self, dt):

    def string_countdown(self, string, format=None):

    # MIDNIGHT

    def utc_datetime_midnight(self, utc_dt=None):

    def utc_seconds_since_midnight(self, utc_dt=None):

    def local_datetime_midnight(self, local_dt=None):

    def local_seconds_since_midnight(self, local_dt=None):

    def datetime_midnight(self, dt=None, utc=False):

    def seconds_since_midnight(self, dt=None, utc=False):

    def seconds_until_midnight(self, dt=None, utc=False, seconds_cast_func=float):

    # AWARE vs. NAIVE

    def is_aware(self, value):

    def is_naive(self, value):

    def make_aware(self, value, timezone=None):

    def make_naive(self, value, timezone=None):

    # PAST vs. FUTURE

    def is_past_time(self, value, base_dt=None, format=None, utc=True):

    def is_future_time(self, value, base_dt=None, format=None, utc=True):

    # YEAR/MONTH/DAY

    def year(self, dt=None, utc=False, timezone=None, idx=0):

    def month(self, dt=None, utc=False, timezone=None, idx=0):

    def day(self, dt=None, utc=False, timezone=None, idx=0):

    def days_of_year(self, year=None, dt=None, idx=0):

    def days_of_month(self, year=None, month=None, dt=None, idx=0):

    # OTHER

    def total_seconds(self, td, ms=True):  # timedelta

    def date_range(self, start_date, end_date, include_end=False, format=None, start_date_format=None, end_date_format=None, return_type='date', return_format=None):

    def week_range(self, start_date, end_date, format=None, start_date_format=None, end_date_format=None, return_type='isoweek', return_format=None):

    def month_range(self, start_date, end_date, format=None, start_date_format=None, end_date_format=None, return_type='date', return_format=None):

    def quarter_range(self, start_date, end_date, format=None, start_date_format=None, end_date_format=None, return_type='date', return_format=None):

    def isoweekdaycount(self, start_date, end_date, isoweekday=7, format=None, start_date_format=None, end_date_format=None):

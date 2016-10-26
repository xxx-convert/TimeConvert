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

    def validate_string(string, format=TIME_FORMAT):

    # REPLACE

    def remove_microsecond(self, dt):

    # DATETIME

    def utc_datetime(ms=True):

    def local_datetime(ms=True, timezone=None):

    def to_utc_datetime(local_dt, timezone=TIME_ZONE):

    def to_local_datetime(utc_dt, timezone=TIME_ZONE):

    def yesterday_utc_datetime(ms=True):

    def tomorrow_utc_datetime(ms=True):

    def yesterday_local_datetime(ms=True, timezone=None):

    def tomorrow_local_datetime(ms=True, timezone=None):

    def several_days_ago(dt=None, utc=True, days=0):

    def several_days_coming(dt=None, utc=True, days=0):

    def several_time_ago(dt=None, utc=True, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):

    def several_time_coming(dt=None, utc=True, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):

    # STRING

    def utc_string(utc_dt=None, format=TIME_FORMAT):

    def local_string(local_dt=None, format=TIME_FORMAT):

    def datetime_to_string(dt, format=TIME_FORMAT):

    # TIMESTAMP

    def utc_timestamp(utc_dt=None):

    def local_timestamp(local_dt=None):

    def datetime_to_timestamp(dt):

    # STRING ==> DATETIME

    def string_to_utc_datetime(string, format=TIME_FORMAT):

    def string_to_local_datetime(string, format=TIME_FORMAT):

    def utc_string_to_utc_datetime(self, utc_string, format=TIME_FORMAT):

    # STRING ==> TIMESTAMP

    def string_to_timestamp(string, format=TIME_FORMAT):

    def string_to_utc_timestamp(string, format=TIME_FORMAT):

    def string_to_local_timestamp(string, format=TIME_FORMAT):

    # TIME_DELTA

    def timestamp_delta(stamp1, stamp2, interval=None):

    def datetime_delta(dt1, dt2, interval=None):

    def string_delta(string1, string2, interval=None, format=TIME_FORMAT, format1='', format2=''):

    PS: interval(seconds) —— Time1 - Time2 >= interval ?

    # TIME_COUNT_DOWN

    def timestamp_countdown(stamp):

    def datetime_countdown(dt):

    def string_countdown(string, format=TIME_FORMAT):

    # MIDNIGHT

    def utc_datetime_midnight(self, utc_dt=None):

    def utc_seconds_since_midnight(self, utc_dt=None):

    def local_datetime_midnight(self, local_dt=None):

    def local_seconds_since_midnight(self, local_dt=None):

    def datetime_midnight(self, dt=None, utc=False):

    def seconds_since_midnight(self, dt=None, utc=False):

    # AWARE vs NAIVE

    def is_aware(value):

    def is_naive(value):

    def make_aware(value, timezone=TIME_ZONE):

    def make_naive(value, timezone=TIME_ZONE):

    # OTHER

    def total_seconds(td):  # timedelta

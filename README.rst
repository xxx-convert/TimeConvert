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

    from TimeConvert import TIME_ZONE, TIME_FORMAT


Method
======

::

    # VALIDATE

    def validate_string(string, format=TIME_FORMAT):

    # REPLACE

    def remove_microsecond(self, dt):

    # DATETIME

    def utc_datetime(ms=True):

    def local_datetime(ms=True):

    def to_utc_datetime(local_dt, timezone=TIME_ZONE):

    def to_local_datetime(utc_dt, timezone=TIME_ZONE):

    def yesterday_utc_datetime():

    def tomorrow_utc_datetime():

    def yesterday_local_datetime():

    def tomorrow_local_datetime():

    def several_days_ago(dt=None, days):

    def several_days_coming(dt=None, days):

    def several_time_ago(dt=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):

    def several_time_coming(dt=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):

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

    # AWARE vs NAIVE

    def is_aware(value):

    def is_naive(value):

    def make_aware(value, timezone=TIME_ZONE):

    def make_naive(value, timezone=TIME_ZONE):

    # OTHER

    def total_seconds(td):  # timedelta

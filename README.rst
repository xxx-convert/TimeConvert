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

Method
======

::

    # DATETIME

    def utc_datetime():

    def local_datetime():

    def to_utc_datetime(local_dt, timezone=TIME_ZONE):

    def to_local_datetime(utc_dt, timezone=TIME_ZONE):

    def yesterday_utc_datetime():

    def tomorrow_utc_datetime():

    def yesterday_local_datetime():

    def tomorrow_local_datetime():

    def several_days_ago(dt, days):

    def several_days_coming(dt, days):

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

    # STRING ==> TIMESTAMP

    def string_to_timestamp(string, format=TIME_FORMAT):

    def string_to_utc_timestamp(string, format=TIME_FORMAT):

    def string_to_local_timestamp(string, format=TIME_FORMAT):

    # OTHERS

    def string_delta(string1, string2, format=TIME_FORMAT, format1='', format2=''):

    # AWARE vs NAIVE

    def is_aware(value):

    def is_naive(value):

    def make_aware(value, timezone=TIME_ZONE):

    def make_naive(value, timezone=TIME_ZONE):

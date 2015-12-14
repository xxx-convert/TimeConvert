# -*- coding: utf-8 -*-

"""
Copyright (c) 2015 HQM <qiminis0801@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import datetime
import pytz
import time


# In [40]: import pytz
# In [41]: pytz.all_timezones
TIME_ZONE = 'Asia/Shanghai'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class _TimeConvert:
    def __init__(self, timezone=None, format=None):
        self.TIME_ZONE = timezone or TIME_ZONE
        self.TIME_FORMAT = format or TIME_FORMAT

    # VALIDATE
    def validate_string(self, string, format=TIME_FORMAT):
        if not string:
            return False
        try:
            time.strptime(string, format)
        except ValueError:
            return False
        return True

    # DATETIME

    def utc_datetime(self):
        return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    def local_datetime(self):
        return self.to_local_datetime(self.utc_datetime())

    def to_local_datetime(self, utc_dt, timezone=TIME_ZONE):
        local = pytz.timezone(timezone)
        utc_dt = utc_dt.replace(tzinfo=pytz.utc)
        return utc_dt.astimezone(local)

    def to_utc_datetime(self, local_dt, timezone=TIME_ZONE):
        local = pytz.timezone(timezone)
        local_dt = local.localize(local_dt, is_dst=None)
        return local_dt.astimezone(pytz.utc)

    def several_days_ago(self, dt=None, days=0):
        return (dt or self.utc_datetime()) - datetime.timedelta(days=days)

    def several_days_coming(self, dt=None, days=0):
        return (dt or self.utc_datetime()) + datetime.timedelta(days=days)

    def several_time_ago(self, dt=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return (dt or self.utc_datetime()) - datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    def several_time_coming(self, dt=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return (dt or self.utc_datetime()) + datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    # STRING

    def utc_string(self, utc_dt=None, format=TIME_FORMAT):
        return self.datetime_to_string(utc_dt or self.utc_datetime(), format)

    def local_string(self, local_dt=None, format=TIME_FORMAT):
        return self.datetime_to_string(local_dt or self.local_datetime(), format)

    def datetime_to_string(self, dt, format=TIME_FORMAT):
        return dt.strftime(format)

    # TIMESTAMP

    def utc_timestamp(self, utc_dt=None):
        return self.datetime_to_timestamp(utc_dt or self.utc_datetime())

    def local_timestamp(self, local_dt=None):
        return self.datetime_to_timestamp(local_dt or self.local_datetime())

    def datetime_to_timestamp(self, dt):
        return int(time.mktime(dt.timetuple()))

    def structime_to_timestamp(self, structime):
        return int(time.mktime(structime))

    # STRING ==> DATETIME

    def string_to_utc_datetime(self, string, format=TIME_FORMAT):
        return self.to_utc_datetime(self.string_to_local_datetime(string, format))

    def string_to_local_datetime(self, string, format=TIME_FORMAT):
        return datetime.datetime.strptime(string, format)

    # STRING ==> TIMESTAMP

    def string_to_timestamp(self, string, format=TIME_FORMAT):
        return self.structime_to_timestamp(time.strptime(string, format))

    def string_to_utc_timestamp(self, string, format=TIME_FORMAT):
        return self.datetime_to_timestamp(self.string_to_utc_datetime(string, format))

    def string_to_local_timestamp(self, string, format=TIME_FORMAT):
        return self.datetime_to_timestamp(self.string_to_local_datetime(string, format))

    # TIME_DELTA

    def timestamp_delta(self, stamp1, stamp2, interval=None):
        delta = stamp1 - stamp2
        abs_delta = abs(delta)
        sign = abs_delta and delta / abs_delta
        delta_seconds = abs_delta % 60
        delta_minutes = abs_delta / 60 % 60
        delta_hours = abs_delta / 3600 % 24
        delta_days = abs_delta / 86400
        delta_weeks = abs_delta / 604800
        return {
            'sign': sign,
            'weeks': delta_weeks,
            'days': delta_days,
            'hours': delta_hours,
            'minutes': delta_minutes,
            'seconds': delta_seconds,
            'total_seconds': abs_delta,
            'delta': delta,
            'count_down_seconds': abs(min(delta, 0)),
            'interval': interval and abs_delta >= interval
        }

    def datetime_delta(self, dt1, dt2, interval=None):
        return self.timestamp_delta(self.datetime_to_timestamp(dt1), self.datetime_to_timestamp(dt2), interval)

    def string_delta(self, string1, string2, interval=None, format=TIME_FORMAT, format1='', format2=''):
        return self.timestamp_delta(self.string_to_timestamp(string1, format1 or format), self.string_to_timestamp(string2, format2 or format), interval)

    # TIME_COUNT_DOWN

    def timestamp_countdown(self, stamp):
        return abs(min((self.utc_timestamp() - stamp), 0))

    def datetime_countdown(self, dt):
        return self.timestamp_countdown(self.datetime_to_timestamp(dt))

    def string_countdown(self, string, format=TIME_FORMAT):
        return self.timestamp_countdown(self.string_to_timestamp(string, format))

    # AWARE vs NAIVE

    # By design, these four functions don't perform any checks on their arguments.
    # The caller should ensure that they don't receive an invalid value like None.

    def is_aware(self, value):
        """
        Determines if a given datetime.datetime is aware.
        The logic is described in Python's docs:
        http://docs.python.org/library/datetime.html#datetime.tzinfo
        """
        return value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None

    def is_naive(self, value):
        """
        Determines if a given datetime.datetime is naive.
        The logic is described in Python's docs:
        http://docs.python.org/library/datetime.html#datetime.tzinfo
        """
        return value.tzinfo is None or value.tzinfo.utcoffset(value) is None

    def make_aware(self, value, timezone=TIME_ZONE):
        """
        Makes a naive datetime.datetime in a given time zone aware.
        """
        timezone = pytz.timezone(timezone)
        if hasattr(timezone, 'localize'):
            # This method is available for pytz time zones.
            return timezone.localize(value, is_dst=None)
        else:
            # Check that we won't overwrite the timezone of an aware datetime.
            if self.is_aware(value):
                raise ValueError(
                    "make_aware expects a naive datetime, got %s" % value)
            # This may be wrong around DST changes!
            return value.replace(tzinfo=timezone)

    def make_naive(self, value, timezone=TIME_ZONE):
        """
        Makes an aware datetime.datetime naive in a given time zone.
        """
        timezone = pytz.timezone(timezone)
        # If `value` is naive, astimezone() will raise a ValueError,
        # so we don't need to perform a redundant check.
        value = value.astimezone(timezone)
        if hasattr(timezone, 'normalize'):
            # This method is available for pytz time zones.
            value = timezone.normalize(value)
        return value.replace(tzinfo=None)


_tc = _TimeConvert()


class TimeConvert:
    def __init__(self, timezone=None, format=None):
        self.TIME_ZONE = timezone or TIME_ZONE
        self.TIME_FORMAT = format or TIME_FORMAT

    # VALIDATE
    @staticmethod
    def validate_string(string, format=TIME_FORMAT):
        return _tc.validate_string(string, format)

    # DATETIME

    @staticmethod
    def utc_datetime():
        return _tc.utc_datetime()

    @staticmethod
    def local_datetime():
        return _tc.local_datetime()

    @staticmethod
    def to_utc_datetime(local_dt, timezone=TIME_ZONE):
        return _tc.to_utc_datetime(local_dt, timezone)

    @staticmethod
    def to_local_datetime(utc_dt, timezone=TIME_ZONE):
        return _tc.to_local_datetime(utc_dt, timezone)

    @staticmethod
    def yesterday_utc_datetime():
        return _tc.several_days_ago(_tc.utc_datetime(), 1)

    @staticmethod
    def tomorrow_utc_datetime():
        return _tc.several_days_coming(_tc.utc_datetime(), 1)

    @staticmethod
    def yesterday_local_datetime():
        return _tc.several_days_ago(_tc.local_datetime(), 1)

    @staticmethod
    def tomorrow_local_datetime():
        return _tc.several_days_coming(_tc.local_datetime(), 1)

    @staticmethod
    def several_days_ago(dt=None, days=0):
        return _tc.several_days_ago(dt, days)

    @staticmethod
    def several_days_coming(dt=None, days=0):
        return _tc.several_days_coming(dt, days)

    @staticmethod
    def several_time_ago(dt=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return _tc.several_time_ago(dt, days, seconds, microseconds, milliseconds, minutes, hours, weeks)

    @staticmethod
    def several_time_coming(dt=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return _tc.several_time_coming(dt, days, seconds, microseconds, milliseconds, minutes, hours, weeks)

    # STRING

    @staticmethod
    def utc_string(utc_dt=None, format=TIME_FORMAT):
        return _tc.utc_string(utc_dt, format)

    @staticmethod
    def local_string(local_dt=None, format=TIME_FORMAT):
        return _tc.local_string(local_dt, format)

    @staticmethod
    def datetime_to_string(dt, format=TIME_FORMAT):
        return dt.strftime(format)

    # TIMESTAMP

    @staticmethod
    def utc_timestamp(utc_dt=None):
        return _tc.utc_timestamp()

    @staticmethod
    def local_timestamp(local_dt=None):
        return _tc.local_timestamp()

    @staticmethod
    def datetime_to_timestamp(dt):
        return _tc.datetime_to_timestamp(dt)

    # STRING ==> DATETIME

    @staticmethod
    def string_to_utc_datetime(string, format=TIME_FORMAT):
        if not _tc.validate_string(string, format):
            return None
        return _tc.string_to_utc_datetime(string, format)

    @staticmethod
    def string_to_local_datetime(string, format=TIME_FORMAT):
        if not _tc.validate_string(string, format):
            return None
        return _tc.string_to_local_datetime(string, format)

    # STRING ==> TIMESTAMP

    @staticmethod
    def string_to_timestamp(string, format=TIME_FORMAT):
        if not _tc.validate_string(string, format):
            return None
        return _tc.string_to_timestamp(string, format)

    @staticmethod
    def string_to_utc_timestamp(string, format=TIME_FORMAT):
        if not _tc.validate_string(string, format):
            return None
        return _tc.string_to_utc_timestamp(string, format)

    @staticmethod
    def string_to_local_timestamp(string, format=TIME_FORMAT):
        if not _tc.validate_string(string, format):
            return None
        return _tc.string_to_local_timestamp(string, format)

    # TIME_DELTA

    @staticmethod
    def timestamp_delta(stamp1, stamp2, interval=None):
        return _tc.timestamp_delta(stamp1, stamp2, interval)

    @staticmethod
    def datetime_delta(dt1, dt2, interval=None):
        return _tc.datetime_delta(dt1, dt2, interval)

    @staticmethod
    def string_delta(string1, string2, interval=None, format=TIME_FORMAT, format1='', format2=''):
        if (not _tc.validate_string(string1, format1 or format)) or (not _tc.validate_string(string2, format2 or format)):
            return None
        return _tc.string_delta(string1, string2, interval, format, format1, format2)

    # TIME_COUNT_DOWN

    @staticmethod
    def timestamp_countdown(stamp):
        return _tc.timestamp_countdown(stamp)

    @staticmethod
    def datetime_countdown(dt):
        return _tc.datetime_countdown(dt)

    @staticmethod
    def string_countdown(string, format=TIME_FORMAT):
        if not _tc.validate_string(string, format):
            return None
        return _tc.string_countdown(string)

    # AWARE vs NAIVE

    # By design, these four functions don't perform any checks on their arguments.
    # The caller should ensure that they don't receive an invalid value like None.

    @staticmethod
    def is_aware(value):
        return _tc.is_aware(value)

    @staticmethod
    def is_naive(value):
        return _tc.is_naive(value)

    @staticmethod
    def make_aware(value, timezone=TIME_ZONE):
        return _tc.make_aware(value, timezone)

    @staticmethod
    def make_naive(value, timezone=TIME_ZONE):
        return _tc.make_naive(value, timezone)

    # OTHER

    @staticmethod
    def total_seconds(td):
        """Total seconds in the duration."""
        return ((td.days * 86400 + td.seconds) * 10 ** 6 + td.microseconds) / 10 ** 6

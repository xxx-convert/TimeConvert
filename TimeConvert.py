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
import time

import pytz

# In [40]: import pytz
# In [41]: pytz.all_timezones
TIME_ZONE = 'Asia/Shanghai'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class TimeConvert:
    def __init__(self, timezone=None, format=None):
        self.TIME_ZONE = timezone or TIME_ZONE
        self.TIME_FORMAT = format or TIME_FORMAT

    # OFFSET

    def offset(self):
        now_timestamp = time.time()
        return datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)

    # VALIDATE

    def validate_string(self, string, format=TIME_FORMAT):
        if not string:
            return False
        try:
            time.strptime(string, format)
        except ValueError:
            return False
        return True

    # REPLACE

    def remove_microsecond(self, dt):
        return dt.replace(microsecond=0)

    # DATETIME

    def utc_datetime(self, ms=True):
        utc_dt = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        return utc_dt if ms else self.remove_microsecond(utc_dt)

    def local_datetime(self, ms=True):
        local_dt = self.to_local_datetime(self.utc_datetime())
        return local_dt if ms else self.remove_microsecond(local_dt)

    def to_utc_datetime(self, local_dt, timezone=TIME_ZONE):
        local = pytz.timezone(timezone)
        local_dt = local.localize(local_dt, is_dst=None)
        return local_dt.astimezone(pytz.utc)

    def to_local_datetime(self, utc_dt, timezone=TIME_ZONE):
        local = pytz.timezone(timezone)
        utc_dt = utc_dt.replace(tzinfo=pytz.utc)
        return utc_dt.astimezone(local)

    def yesterday_utc_datetime(self):
        return self.several_days_ago(self.utc_datetime(), 1)

    def tomorrow_utc_datetime(self):
        return self.several_days_coming(self.utc_datetime(), 1)

    def yesterday_local_datetime(self):
        return self.several_days_ago(self.local_datetime(), 1)

    def tomorrow_local_datetime(self):
        return self.several_days_coming(self.local_datetime(), 1)

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
        if not self.validate_string(string, format):
            return None
        return self.to_utc_datetime(self.string_to_local_datetime(string, format))

    def string_to_local_datetime(self, string, format=TIME_FORMAT):
        if not self.validate_string(string, format):
            return None
        return datetime.datetime.strptime(string, format)

    def utc_string_to_utc_datetime(self, utc_string, format=TIME_FORMAT):
        if not self.validate_string(utc_string, format):
            return None
        return self.to_utc_datetime(self.string_to_local_datetime(utc_string, format)) + self.offset()

    # STRING ==> TIMESTAMP

    def string_to_timestamp(self, string, format=TIME_FORMAT):
        if not self.validate_string(string, format):
            return None
        return self.structime_to_timestamp(time.strptime(string, format))

    def string_to_utc_timestamp(self, string, format=TIME_FORMAT):
        if not self.validate_string(string, format):
            return None
        return self.datetime_to_timestamp(self.string_to_utc_datetime(string, format))

    def string_to_local_timestamp(self, string, format=TIME_FORMAT):
        if not self.validate_string(string, format):
            return None
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
        if (not self.validate_string(string1, format1 or format)) or (not self.validate_string(string2, format2 or format)):
            return None
        return self.timestamp_delta(self.string_to_timestamp(string1, format1 or format), self.string_to_timestamp(string2, format2 or format), interval)

    # TIME_COUNT_DOWN

    def timestamp_countdown(self, stamp):
        return abs(min((self.utc_timestamp() - stamp), 0))

    def datetime_countdown(self, dt):
        return self.timestamp_countdown(self.datetime_to_timestamp(dt))

    def string_countdown(self, string, format=TIME_FORMAT):
        if not self.validate_string(string, format):
            return None
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

    # OTHER

    def total_seconds(self, td):
        """Total seconds in the duration."""
        return ((td.days * 86400 + td.seconds) * 10 ** 6 + td.microseconds) / 10 ** 6


TimeConvert = TimeConvert()

# -*- coding: utf-8 -*-

from __future__ import division

import calendar
import datetime
import locale
import time

import pytz
import tzlocal
from dateutil.relativedelta import relativedelta

from .compat import basestring, is_py2


class TimeConvert:
    def __init__(self, timezone=None, format=None):
        self.BASE_TIME_ZONE = tzlocal.get_localzone().zone
        self.BASE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        self.TIME_ZONE = timezone or self.BASE_TIME_ZONE
        self.TIME_FORMAT = format or self.BASE_TIME_FORMAT
        self.SECOND_MILLISECOND = 10 ** 3
        self.SECOND_MICROSECOND = 10 ** 6

    def timezone(self, timezone=None):
        # In [1]: import pytz
        # In [2]: pytz.all_timezones
        return timezone or self.TIME_ZONE

    def format(self, format=None):
        return format or self.TIME_FORMAT

    # PRIVATE

    def __utc_datetime(self, utc_dt=None, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return self.several_time_coming(dt=utc_dt or self.basic_utc_datetime(), utc=True, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    def __local_datetime(self, local_dt=None, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return self.several_time_coming(dt=local_dt or self.basic_local_datetime(), utc=False, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    def __datetime(self, dt=None, utc=True, timezone=None):
        return dt or (self.basic_utc_datetime() if utc else self.basic_local_datetime(timezone=timezone))

    def __remove_ms_or_not(self, dt=None, ms=True):
        return dt if ms else self.remove_microsecond(dt)

    def __seconds_to_other(self, s, base=0):
        return int(s * (base or self.SECOND_MICROSECOND))

    # OFFSET

    def offset(self):
        now_timestamp = time.time()
        return datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)

    # VALIDATE

    def validate_string(self, string, format=None):
        if not string:
            return False
        try:
            time.strptime(string, self.format(format))
        except ValueError:
            return False
        return True

    # REPLACE

    def remove_microsecond(self, dt):
        return dt.replace(microsecond=0) if hasattr(dt, 'replace') else dt

    # BASIC DATETIME

    def basic_utc_datetime(self, ms=True):
        return self.__remove_ms_or_not(datetime.datetime.utcnow().replace(tzinfo=pytz.utc), ms=ms)

    def basic_local_datetime(self, ms=True, timezone=None):
        # In[1]: import time
        #
        # In[2]: time.localtime()
        # Out[2]: time.struct_time(tm_year=2017, tm_mon=4, tm_mday=3, tm_hour=23, tm_min=19, tm_sec=39, tm_wday=0, tm_yday=93, tm_isdst=0)
        #
        # In[3]: time.localtime(time.time())
        # Out[3]: time.struct_time(tm_year=2017, tm_mon=4, tm_mday=3, tm_hour=23, tm_min=19, tm_sec=40, tm_wday=0, tm_yday=93, tm_isdst=0)
        #
        # In[4]: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # Out[4]: '2017-04-03 23:19:57'
        #
        # In[5]: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # Out[5]: '2017-04-03 23:20:00'
        return self.__remove_ms_or_not(self.to_local_datetime(self.basic_utc_datetime(), self.timezone(timezone)), ms=ms)

    def is_utc_datetime(self, dt):
        return dt.tzinfo == pytz.utc

    def is_local_datetime(self, dt, local_tz=None):
        """
        Check whether local datetime or not.

        ``local_tz`` indicates local tzinfo.
            ``local_dt`` is ``None``: get_localzone from system.
            ``local_dt`` is ``-1``: local tzinfo is ``None``.
        """
        # In [1]: pytz.timezone('Asia/Shanghai')
        # Out[1]: <DstTzInfo 'Asia/Shanghai' LMT+8:06:00 STD>

        # In [2]: tc.local_datetime().tzinfo
        # Out[2]: <DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>

        # In [3]: pytz.timezone('Asia/Shanghai') == tc.local_datetime().tzinfo
        # Out[3]: False

        # In [4]: str(pytz.timezone('Asia/Shanghai')) == str(tc.local_datetime().tzinfo)
        # Out[4]: True

        return str(dt.tzinfo) == str(None if local_tz == -1 else self.timezone(local_tz))

    def to_utc_datetime(self, dt, timezone=None):
        if self.is_utc_datetime(dt):
            return dt
        try:
            dt = self.make_naive(dt)
        except ValueError:
            pass
        local_tz = pytz.timezone(self.timezone(timezone))
        local_dt = local_tz.localize(dt, is_dst=None)
        return local_dt.astimezone(pytz.utc)

    def to_local_datetime(self, dt, timezone=None):
        tzname = self.timezone(timezone)
        if self.is_local_datetime(dt, local_tz=tzname):
            return dt
        local_tz = pytz.timezone(tzname)
        utc_dt = dt.replace(tzinfo=pytz.utc)
        return utc_dt.astimezone(local_tz)

    # DATE
    def utc_date(self, dt=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return self.datetime_to_date(self.utc_datetime(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks))

    def local_date(self, dt=None, utc=False, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return self.datetime_to_date(self.local_datetime(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks))

    def datetime_to_date(self, dt):
        return datetime.datetime.date(dt)

    def is_the_same_day(self, dt1, dt2):
        return self.local_string(dt1, format='%Y-%m-%d') == self.local_string(dt2, format='%Y-%m-%d')

    # DATETIME

    def yesterday_utc_datetime(self, ms=True):
        return self.__remove_ms_or_not(self.several_days_ago(days=1), ms=ms)

    def tomorrow_utc_datetime(self, ms=True):
        return self.__remove_ms_or_not(self.several_days_coming(days=1), ms=ms)

    def yesterday_local_datetime(self, ms=True, timezone=None):
        return self.__remove_ms_or_not(self.several_days_ago(utc=False, timezone=timezone, days=1), ms=ms)

    def tomorrow_local_datetime(self, ms=True, timezone=None):
        return self.__remove_ms_or_not(self.several_days_coming(utc=False, timezone=timezone, days=1), ms=ms)

    def several_days_ago(self, dt=None, utc=True, ms=True, timezone=None, days=0):
        return self.__remove_ms_or_not(self.__datetime(dt, utc, timezone=timezone) - datetime.timedelta(days=days), ms=ms)

    def several_days_coming(self, dt=None, utc=True, ms=True, timezone=None, days=0):
        return self.__remove_ms_or_not(self.__datetime(dt, utc, timezone=timezone) + datetime.timedelta(days=days), ms=ms)

    def several_time_ago(self, dt=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return self.__remove_ms_or_not(self.__datetime(dt, utc, timezone=timezone) - relativedelta(years=years, months=months) - datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), ms=ms)

    def several_time_coming(self, dt=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return self.__remove_ms_or_not(self.__datetime(dt, utc, timezone=timezone) + relativedelta(years=years, months=months) + datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), ms=ms)

    def utc_datetime(self, dt=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return self.several_time_coming(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    def local_datetime(self, dt=None, utc=False, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return self.several_time_coming(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    # STRING

    def datetime_to_unicode_string(self, dt, format=None):
        format = self.format(format)
        # Refer: https://github.com/sphinx-doc/sphinx/blob/8ae43b9fd/sphinx/util/osutil.py#L164
        if is_py2:
            # if a locale is set, the time strings are encoded in the encoding
            # given by LC_TIME; if that is available, use it
            enc = locale.getlocale(locale.LC_TIME)[1] or 'utf-8'
            return dt.strftime(unicode(format).encode(enc)).decode(enc)
        else:  # Py3
            # On Windows, time.strftime() and Unicode characters will raise UnicodeEncodeError.
            # http://bugs.python.org/issue8304
            try:
                return dt.strftime(format)
            except UnicodeEncodeError:
                return dt.strftime(format.encode('unicode-escape').decode()).encode().decode('unicode-escape')

    def datetime_to_string(self, dt, format=None, isuc=False):
        if isuc:
            return self.datetime_to_unicode_string(dt, format=format)
        return dt.strftime(self.format(format))

    def yesterday_utc_string(self, format=None, ms=True, isuc=False):
        return self.datetime_to_string(self.yesterday_utc_datetime(ms=ms), self.format(format), isuc=isuc)

    def tomorrow_utc_string(self, format=None, ms=True, isuc=False):
        return self.datetime_to_string(self.tomorrow_utc_datetime(ms=ms), self.format(format), isuc=isuc)

    def yesterday_local_string(self, format=None, ms=True, timezone=None, isuc=False):
        return self.datetime_to_string(self.yesterday_local_datetime(ms=ms, timezone=timezone), self.format(format), isuc=isuc)

    def tomorrow_local_string(self, format=None, ms=True, timezone=None, isuc=False):
        return self.datetime_to_string(self.tomorrow_local_datetime(ms=ms, timezone=timezone), self.format(format), isuc=isuc)

    def several_days_ago_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, days=0, isuc=False):
        return self.datetime_to_string(self.several_days_ago(dt=dt, utc=utc, ms=ms, timezone=timezone, days=days), self.format(format), isuc=isuc)

    def several_days_coming_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, days=0, isuc=False):
        return self.datetime_to_string(self.several_days_coming(dt=dt, utc=utc, ms=ms, timezone=timezone, days=days), self.format(format), isuc=isuc)

    def several_time_ago_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, isuc=False):
        return self.datetime_to_string(self.several_time_ago(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), self.format(format), isuc=isuc)

    def several_time_coming_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, isuc=False):
        return self.datetime_to_string(self.several_time_coming(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), self.format(format), isuc=isuc)

    def utc_string(self, dt=None, format=None, utc=True, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, local_dt=None, utc_dt=None, isuc=False):
        final_dt = dt or utc_dt
        final_dt = self.utc_datetime(dt=local_dt) if not final_dt and local_dt else final_dt
        return self.datetime_to_string(self.utc_datetime(dt=final_dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), self.format(format), isuc=isuc)

    def local_string(self, dt=None, format=None, utc=False, ms=True, timezone=None, years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, local_dt=None, utc_dt=None, isuc=False):
        final_dt = dt or local_dt
        final_dt = self.to_local_datetime(dt=utc_dt) if not final_dt and utc_dt else final_dt
        return self.datetime_to_string(self.local_datetime(dt=final_dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), self.format(format), isuc=isuc)

    # TIMESTAMP

    def __micro_or_milli(self, s, micro=False, milli=False):
        if micro:
            return self.seconds_to_microseconds(s)
        if milli:
            return self.seconds_to_milliseconds(s)
        return s

    def utc_timestamp(self, utc_dt=None, ms=False, micro=False, milli=False):
        return self.__micro_or_milli(self.datetime_to_timestamp(self.__utc_datetime(utc_dt), ms=ms), micro=micro, milli=milli)

    def local_timestamp(self, local_dt=None, ms=False, micro=False, milli=False):
        return self.__micro_or_milli(self.datetime_to_timestamp(self.__local_datetime(local_dt), ms=ms), micro=micro, milli=milli)

    def datetime_to_timestamp(self, dt, ms=False):
        # http://stackoverflow.com/questions/26161156/python-converting-string-to-timestamp-with-microseconds
        # ``dt - epoch`` will raise ``TypeError: can't subtract offset-naive and offset-aware datetimes``
        # Total seconds from ``1970-01-01 00:00:00``(utc or local)
        # Different from definition of timestamp(时间戳是指格林威治时间1970年01月01日00时00分00秒(北京时间1970年01月01日08时00分00秒)起至现在的总秒数)
        stamp = self.structime_to_timestamp(dt.timetuple())
        if not ms:
            return stamp
        return stamp + dt.microsecond / self.SECOND_MICROSECOND

    def structime_to_timestamp(self, structime):
        return int(time.mktime(structime))

    def seconds_to_microseconds(self, s):
        return self.__seconds_to_other(s, base=self.SECOND_MICROSECOND)

    def seconds_to_milliseconds(self, s):
        return self.__seconds_to_other(s, base=self.SECOND_MILLISECOND)

    # STRING ==> DATETIME

    def string_to_datetime(self, string, format=None):
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return datetime.datetime.strptime(string, format)

    def string_to_utc_datetime(self, string, format=None):
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return self.to_utc_datetime(self.string_to_datetime(string, format))

    def string_to_local_datetime(self, string, format=None):
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return self.to_local_datetime(self.string_to_datetime(string, format)) - self.offset()

    def utc_string_to_utc_datetime(self, utc_string, format=None):
        format = self.format(format)
        if not self.validate_string(utc_string, format):
            return None
        return self.to_utc_datetime(self.string_to_datetime(utc_string, format)) + self.offset()

    def utc_string_to_local_datetime(self, utc_string, format=None):
        format = self.format(format)
        if not self.validate_string(utc_string, format):
            return None
        return self.to_local_datetime(self.string_to_datetime(utc_string, format))

    # STRING ==> TIMESTAMP

    def string_to_timestamp(self, string, format=None, ms=False):
        return self.string_to_local_timestamp(string, format, ms=ms)

    def string_to_utc_timestamp(self, string, format=None, ms=False):
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return self.datetime_to_timestamp(self.string_to_utc_datetime(string, format), ms=ms)

    def string_to_local_timestamp(self, string, format=None, ms=False):
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return self.datetime_to_timestamp(self.string_to_local_datetime(string, format), ms=ms)

    # TIME_DELTA

    def timestamp_delta(self, stamp1, stamp2, interval=None):
        delta = stamp1 - stamp2
        abs_delta = abs(delta)
        sign = abs_delta and delta // abs_delta
        delta_seconds = abs_delta % 60
        delta_minutes = abs_delta // 60 % 60
        delta_hours = abs_delta // 3600 % 24
        delta_days = abs_delta // 86400
        delta_weeks = abs_delta // 604800
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

    def string_delta(self, string1, string2, interval=None, format=None, format1=None, format2=None):
        format = self.format(format)
        if (not self.validate_string(string1, format1 or format)) or (not self.validate_string(string2, format2 or format)):
            return None
        return self.timestamp_delta(self.string_to_timestamp(string1, format1 or format), self.string_to_timestamp(string2, format2 or format), interval)

    # TIME_COUNT_DOWN

    def timestamp_countdown(self, stamp):
        return abs(min((self.utc_timestamp() - stamp), 0))

    def datetime_countdown(self, dt):
        return self.timestamp_countdown(self.datetime_to_timestamp(dt))

    def string_countdown(self, string, format=None):
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return self.timestamp_countdown(self.string_to_timestamp(string, format))

    # MIDNIGHT

    def utc_datetime_midnight(self, utc_dt=None):
        return (self.__utc_datetime(utc_dt)).replace(hour=0, minute=0, second=0, microsecond=0)

    def utc_seconds_since_midnight(self, utc_dt=None, seconds_cast_func=float):
        utc_dt = self.__utc_datetime(utc_dt)
        return seconds_cast_func(self.total_seconds(utc_dt - self.utc_datetime_midnight(utc_dt)))

    def local_datetime_midnight(self, local_dt=None):
        return (self.__local_datetime(local_dt)).replace(hour=0, minute=0, second=0, microsecond=0)

    def local_seconds_since_midnight(self, local_dt=None, seconds_cast_func=float):
        local_dt = self.__local_datetime(local_dt)
        return seconds_cast_func(self.total_seconds(local_dt - self.local_datetime_midnight(local_dt)))

    def datetime_midnight(self, dt=None, utc=False):
        return self.utc_datetime_midnight(dt) if utc else self.local_datetime_midnight(dt)

    def seconds_since_midnight(self, dt=None, utc=False, seconds_cast_func=float):
        return seconds_cast_func(self.utc_seconds_since_midnight(dt) if utc else self.local_seconds_since_midnight(dt))

    def seconds_until_midnight(self, dt=None, utc=False, seconds_cast_func=float):
        return seconds_cast_func(86400 - self.seconds_since_midnight(dt=dt, utc=utc))

    # AWARE vs. NAIVE

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

    def make_aware(self, value, timezone=None):
        """
        Makes a naive datetime.datetime in a given time zone aware.
        """
        timezone = pytz.timezone(self.timezone(timezone))
        if hasattr(timezone, 'localize'):
            # This method is available for pytz time zones.
            return timezone.localize(value, is_dst=None)
        else:
            # Check that we won't overwrite the timezone of an aware datetime.
            if self.is_aware(value):
                raise ValueError('make_aware expects a naive datetime, got %s' % value)
            # This may be wrong around DST changes!
        return value.replace(tzinfo=timezone)

    def make_naive(self, value, timezone=None):
        """
        Makes an aware datetime.datetime naive in a given time zone.
        """
        timezone = pytz.timezone(self.timezone(timezone))
        # If `value` is naive, astimezone() will raise a ValueError,
        # so we don't need to perform a redundant check.
        value = value.astimezone(timezone)
        if hasattr(timezone, 'normalize'):
            # This method is available for pytz time zones.
            value = timezone.normalize(value)
        return value.replace(tzinfo=None)

    # PAST vs. FUTURE

    def is_past_time(self, value, base_dt=None, format=None, utc=True):
        base_dt = base_dt or self.basic_utc_datetime()

        if not value:
            return None

        if isinstance(value, datetime.datetime):
            return (value if utc else self.to_local_datetime(value)) < base_dt

        if isinstance(value, basestring):
            utc_dt = self.utc_string_to_utc_datetime(value, format=format) if utc else self.string_to_utc_datetime(value, format=format)
            return utc_dt and utc_dt < base_dt

        if isinstance(value, int):
            stamp = self.datetime_to_timestamp(base_dt if utc else self.to_local_datetime(base_dt), ms=True)
            return value < stamp

        return None

    def is_future_time(self, value, base_dt=None, format=None, utc=True):
        base_dt = base_dt or self.basic_utc_datetime()

        if not value:
            return None

        if isinstance(value, datetime.datetime):
            return (value if utc else self.to_local_datetime(value)) > base_dt

        if isinstance(value, basestring):
            utc_dt = self.utc_string_to_utc_datetime(value, format=format) if utc else self.string_to_utc_datetime(value, format=format)
            return utc_dt and utc_dt > base_dt

        if isinstance(value, int):
            stamp = self.datetime_to_timestamp(base_dt if utc else self.to_local_datetime(base_dt), ms=True)
            return value > stamp

        return None

    # YEAR/MONTH/DAY
    def year(self, dt=None, utc=False, timezone=None, idx=0):
        return self.__datetime(dt=self.several_time_coming(dt=dt, utc=utc, timezone=timezone, years=idx), utc=utc).year

    def month(self, dt=None, utc=False, timezone=None, idx=0):
        return self.__datetime(dt=self.several_time_coming(dt=dt, utc=utc, timezone=timezone, months=idx), utc=utc).month

    def day(self, dt=None, utc=False, timezone=None, idx=0):
        return self.__datetime(dt=self.several_time_coming(dt=dt, utc=utc, timezone=timezone, days=idx), utc=utc).day

    def days_of_year(self, year=None, dt=None, idx=0):
        return 366 if calendar.isleap(year or self.year(dt, idx=idx)) else 365

    def days_of_month(self, year=None, month=None, dt=None, idx=0):
        return calendar.monthrange(year=(year or self.year(dt, idx=idx)), month=(month or self.month(dt, idx=idx)))[-1]

    # OTHER

    def total_seconds(self, td, ms=True):
        """Total seconds in the duration."""
        if not ms:
            return td.days * 86400 + td.seconds
        return ((td.days * 86400 + td.seconds) * self.SECOND_MICROSECOND + td.microseconds) / self.SECOND_MICROSECOND


TimeConvert = TimeConvert()

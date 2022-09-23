import calendar
import datetime
import time
from typing import Any, Callable, Dict, Optional, TypeVar, Union

import tzlocal
from dateutil.relativedelta import relativedelta
from dateutil.tz import tz
from isoweek import Week

from .month import Month
from .quarter import Quarter


T = TypeVar('T')


class TimeConvertTools(object):
    def __get_base_time_zone(self):
        if hasattr(tzlocal, 'get_localzone_name'):
            return tzlocal.get_localzone_name()
        tz_localzone = tzlocal.get_localzone()
        if hasattr(tz_localzone, 'unwrap_shim'):
            tz_localzone = tz_localzone.unwrap_shim()
        return tz_localzone.key if hasattr(tz_localzone, 'key') else tz_localzone.zone

    def __init__(self, timezone: Optional[str] = None, format: Optional[str] = None):
        self.BASE_TIME_ZONE = self.__get_base_time_zone()
        self.DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        self.DATE_FORMAT = '%Y-%m-%d'
        self.WEEK_FORMAT = '%W'
        self.WEEK_FORMAT_U = '%U'
        self.WEEK_FORMAT_W = '%W'
        self.WEEK_FORMAT_ISO = 'ISO'
        self.MODE_WEEK_FORMAT = {
            0: self.WEEK_FORMAT_U,
            5: self.WEEK_FORMAT_W,
            3: self.WEEK_FORMAT_ISO,
        }
        self.LEN_FORMAT = {
            19: self.DATETIME_FORMAT,
            10: self.DATE_FORMAT,
        }
        self.TIME_ZONE = timezone or self.BASE_TIME_ZONE
        self.TIME_FORMAT = format or self.DATETIME_FORMAT
        self.SECOND_MILLISECOND = 10 ** 3
        self.SECOND_MICROSECOND = 10 ** 6

    def timezone(self, timezone: Optional[str] = None) -> str:
        # In [1]: import pytz
        # In [2]: pytz.all_timezones
        return timezone or self.TIME_ZONE

    def format(self, format: Optional[str] = None) -> str:
        return format or self.TIME_FORMAT

    def date_format(self, format: Optional[str] = None) -> str:
        return format or self.DATE_FORMAT

    def value_format(self, value: Optional[str] = None, format: Optional[str] = None) -> str:
        if format:
            return format
        return self.LEN_FORMAT.get(len(value))

    # PRIVATE

    def __utc_datetime(self, utc_dt: Optional[datetime.datetime] = None, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> datetime.datetime:
        return self.several_time_coming(dt=utc_dt or self.basic_utc_datetime(), utc=True, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    def __local_datetime(self, local_dt: Optional[datetime.datetime] = None, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> datetime.datetime:
        return self.several_time_coming(dt=local_dt or self.basic_local_datetime(), utc=False, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    def __datetime(self, dt: Optional[datetime.datetime] = None, utc: Optional[bool] = True, timezone: Optional[str] = None) -> datetime.datetime:
        return dt or (self.basic_utc_datetime() if utc else self.basic_local_datetime(timezone=timezone))

    def __remove_ms_or_not(self, dt: datetime.datetime, ms: Optional[bool] = True) -> datetime.datetime:
        return dt if ms else self.remove_microsecond(dt)

    def __seconds_to_other(self, s: int, base: int = 0) -> int:
        return int(s * (base or self.SECOND_MICROSECOND))

    # OFFSET

    def offset(self) -> int:
        now_timestamp = time.time()
        return datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)

    # VALIDATE

    def validate_string(self, string: str, format: Optional[str] = None) -> bool:
        if not string:
            return False
        try:
            time.strptime(string, self.format(format))
        except ValueError:
            return False
        return True

    # REPLACE

    def remove_microsecond(self, dt: datetime.datetime) -> datetime.datetime:
        return dt.replace(microsecond=0) if hasattr(dt, 'replace') else dt

    # BASIC DATETIME

    def basic_utc_datetime(self, ms: bool = True) -> datetime.datetime:
        return self.__remove_ms_or_not(datetime.datetime.utcnow().replace(tzinfo=tz.UTC), ms=ms)

    def basic_local_datetime(self, ms: bool = True, timezone: Optional[str] = None) -> datetime.datetime:
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

    def is_utc_datetime(self, dt: datetime.datetime) -> bool:
        return dt.tzinfo == tz.UTC

    def is_local_datetime(self, dt: datetime.datetime, local_tz: Optional[str] = None) -> bool:
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

        return str(dt.tzinfo) == str(None if local_tz == -1 else tz.gettz(self.timezone(local_tz)))

    def to_utc_datetime(self, dt: datetime.datetime, timezone: Optional[str] = None) -> datetime.datetime:
        if self.is_utc_datetime(dt):
            return dt
        try:
            dt = self.make_naive(dt)
        except ValueError:
            pass
        tzinfo = tz.gettz(self.timezone(timezone))
        local_dt = dt.replace(tzinfo=tzinfo)
        return local_dt.astimezone(tz.UTC)

    def to_local_datetime(self, dt: datetime.datetime, timezone: Optional[str] = None) -> datetime.datetime:
        tzname = self.timezone(timezone)
        if self.is_local_datetime(dt, local_tz=tzname):
            return dt
        tzinfo = tz.gettz(tzname)
        utc_dt = dt.replace(tzinfo=tz.UTC)
        return utc_dt.astimezone(tzinfo)

    # DATETIME

    def yesterday_utc_datetime(self, ms: bool = True) -> datetime.datetime:
        return self.__remove_ms_or_not(self.several_days_ago(days=1), ms=ms)

    def tomorrow_utc_datetime(self, ms: bool = True) -> datetime.datetime:
        return self.__remove_ms_or_not(self.several_days_coming(days=1), ms=ms)

    def yesterday_local_datetime(self, ms: bool = True, timezone: Optional[str] = None) -> datetime.datetime:
        return self.__remove_ms_or_not(self.several_days_ago(utc=False, timezone=timezone, days=1), ms=ms)

    def tomorrow_local_datetime(self, ms: bool = True, timezone: Optional[str] = None) -> datetime.datetime:
        return self.__remove_ms_or_not(self.several_days_coming(utc=False, timezone=timezone, days=1), ms=ms)

    def several_days_ago(self, dt: Optional[datetime.datetime] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, days: int = 0) -> datetime.datetime:
        return self.__remove_ms_or_not(self.__datetime(dt, utc, timezone=timezone) - datetime.timedelta(days=days), ms=ms)

    def several_days_coming(self, dt: Optional[datetime.datetime] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, days: int = 0) -> datetime.datetime:
        return self.__remove_ms_or_not(self.__datetime(dt, utc, timezone=timezone) + datetime.timedelta(days=days), ms=ms)

    def several_time_ago(self, dt: Optional[datetime.datetime] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> datetime.datetime:
        return self.__remove_ms_or_not(self.__datetime(dt, utc, timezone=timezone) - relativedelta(years=years, months=months) - datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), ms=ms)

    def several_time_coming(self, dt: Optional[datetime.datetime] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> datetime.datetime:
        return self.__remove_ms_or_not(self.__datetime(dt, utc, timezone=timezone) + relativedelta(years=years, months=months) + datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), ms=ms)

    def utc_datetime(self, dt: Optional[datetime.datetime] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> datetime.datetime:
        return self.several_time_coming(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    def local_datetime(self, dt: Optional[datetime.datetime] = None, utc: bool = False, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> datetime.datetime:
        return self.several_time_coming(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    # DATE

    def utc_date(self, dt: Optional[datetime.datetime] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> datetime.date:
        return self.datetime_to_date(self.utc_datetime(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks))

    def local_date(self, dt: Optional[datetime.datetime] = None, utc: bool = False, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> datetime.date:
        return self.datetime_to_date(self.local_datetime(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks))

    def datetime_to_date(self, dt: datetime.datetime) -> datetime.date:
        # return datetime.datetime.date(dt)
        return dt.date()

    def to_date(self, value: Union[str, datetime.datetime, datetime.date], format: Optional[str] = None, idx: int = 0) -> Optional[datetime.date]:
        if isinstance(value, datetime.datetime):
            date = self.datetime_to_date(value)
        elif isinstance(value, datetime.date):
            date = value
        elif isinstance(value, (str, bytes)):
            date = self.string_to_date(value, format)
        else:
            return None
        return date + datetime.timedelta(days=idx)

    # def is_the_same_day(self, dt1: datetime.date, dt2: datetime.date) -> bool:
    #     return self.local_string(dt1, format=self.DATE_FORMAT) == self.local_string(dt2, format=self.DATE_FORMAT)
    def is_the_same_day(self, value1: Union[str, datetime.datetime, datetime.date], value2: Union[str, datetime.datetime, datetime.date], format: Optional[str] = None, format1: Optional[str] = None, format2: Optional[str] = None) -> bool:
        return self.to_date(value1, format=format1 or format) == self.to_date(value2, format=format2 or format)

    # WEEK

    def utc_week(self, dt: Optional[datetime.datetime] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False, mode: int = 3) -> str:
        week_format = self.MODE_WEEK_FORMAT.get(mode, self.WEEK_FORMAT_ISO)
        if week_format != self.WEEK_FORMAT_ISO:
            return int(self.utc_string(dt=dt, format=week_format, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks, local_dt=local_dt, utc_dt=utc_dt, isuc=isuc))
        return Week.withdate(self.utc_date(dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)).week

    def local_week(self, dt: Optional[datetime.datetime] = None, utc: bool = False, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False, mode: int = 3) -> str:
        week_format = self.MODE_WEEK_FORMAT.get(mode, self.WEEK_FORMAT_ISO)
        if week_format != self.WEEK_FORMAT_ISO:
            return int(self.local_string(dt=dt, format=week_format, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks, local_dt=local_dt, utc_dt=utc_dt, isuc=isuc))
        return Week.withdate(self.local_date(dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)).week

    def to_week(self, value: Union[str, datetime.datetime, datetime.date], format: Optional[str] = None, idx: int = 0) -> Optional[Week]:
        date = self.to_date(value, format=format)
        if not date:
            return None
        return Week.withdate(date) + idx

    to_isoweek = to_week

    # STRING

    # DATETIME_STRING
    def datetime_to_unicode_string(self, dt: datetime.datetime, format: Optional[str] = None) -> str:
        format = self.format(format)
        # Refer: https://github.com/sphinx-doc/sphinx/blob/8ae43b9fd/sphinx/util/osutil.py#L164
        # On Windows, time.strftime() and Unicode characters will raise UnicodeEncodeError.
        # http://bugs.python.org/issue8304
        try:
            return dt.strftime(format)
        except UnicodeEncodeError:
            return dt.strftime(format.encode('unicode-escape').decode()).encode().decode('unicode-escape')

    def datetime_to_string(self, dt: datetime.datetime, format: Optional[str] = None, isuc: bool = False) -> str:
        if isuc:
            return self.datetime_to_unicode_string(dt, format=format)
        return dt.strftime(self.format(format))

    def yesterday_utc_string(self, format: Optional[str] = None, ms: bool = True, isuc: bool = False) -> str:
        return self.datetime_to_string(self.yesterday_utc_datetime(ms=ms), self.format(format), isuc=isuc)

    def tomorrow_utc_string(self, format: Optional[str] = None, ms: bool = True, isuc: bool = False) -> str:
        return self.datetime_to_string(self.tomorrow_utc_datetime(ms=ms), self.format(format), isuc=isuc)

    def yesterday_local_string(self, format: Optional[str] = None, ms: bool = True, timezone: Optional[str] = None, isuc: bool = False) -> str:
        return self.datetime_to_string(self.yesterday_local_datetime(ms=ms, timezone=timezone), self.format(format), isuc=isuc)

    def tomorrow_local_string(self, format: Optional[str] = None, ms: bool = True, timezone: Optional[str] = None, isuc: bool = False) -> str:
        return self.datetime_to_string(self.tomorrow_local_datetime(ms=ms, timezone=timezone), self.format(format), isuc=isuc)

    def several_days_ago_string(self, dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, days: int = 0, isuc: bool = False) -> str:
        return self.datetime_to_string(self.several_days_ago(dt=dt, utc=utc, ms=ms, timezone=timezone, days=days), self.format(format), isuc=isuc)

    def several_days_coming_string(self, dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, days: int = 0, isuc: bool = False) -> str:
        return self.datetime_to_string(self.several_days_coming(dt=dt, utc=utc, ms=ms, timezone=timezone, days=days), self.format(format), isuc=isuc)

    def several_time_ago_string(self, dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, isuc: bool = False) -> str:
        return self.datetime_to_string(self.several_time_ago(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), self.format(format), isuc=isuc)

    def several_time_coming_string(self, dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, isuc: bool = False) -> str:
        return self.datetime_to_string(self.several_time_coming(dt=dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), self.format(format), isuc=isuc)

    def utc_string(self, dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False) -> str:
        final_dt = dt or utc_dt
        final_dt = self.utc_datetime(dt=local_dt) if not final_dt and local_dt else final_dt
        return self.datetime_to_string(self.utc_datetime(dt=final_dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), self.format(format), isuc=isuc)

    def local_string(self, dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = False, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False) -> str:
        final_dt = dt or local_dt
        final_dt = self.to_local_datetime(dt=utc_dt) if not final_dt and utc_dt else final_dt
        return self.datetime_to_string(self.local_datetime(dt=final_dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), self.format(format), isuc=isuc)

    def utc_datetime_string(self, dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False) -> str:
        return self.utc_string(dt=dt, format=self.format(format), utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks, local_dt=local_dt, utc_dt=utc_dt, isuc=isuc)

    def local_datetime_string(self, dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = False, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False) -> str:
        return self.local_string(dt=dt, format=self.format(format), utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks, local_dt=local_dt, utc_dt=utc_dt, isuc=isuc)

    # DATE_STRING
    def utc_date_string(self, dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False) -> str:
        return self.utc_string(dt=dt, format=self.date_format(format), utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks, local_dt=local_dt, utc_dt=utc_dt, isuc=isuc)

    def local_date_string(self, dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = False, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False) -> str:
        return self.local_string(dt=dt, format=self.date_format(format), utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks, local_dt=local_dt, utc_dt=utc_dt, isuc=isuc)

    # WEEK_STRING
    def utc_week_string(self, dt: Optional[datetime.datetime] = None, utc: bool = True, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False, mode: int = 3) -> str:
        return str(self.utc_week(dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks))

    def local_week_string(self, dt: Optional[datetime.datetime] = None, utc: bool = False, ms: bool = True, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0, local_dt: Optional[datetime.datetime] = None, utc_dt: Optional[datetime.datetime] = None, isuc: bool = False, mode: int = 3) -> str:
        return str(self.local_week(dt, utc=utc, ms=ms, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks))

    # TIMESTAMP

    def __micro_or_milli(self, s, micro: bool = False, milli: bool = False) -> int:
        if micro:
            return self.seconds_to_microseconds(s)
        if milli:
            return self.seconds_to_milliseconds(s)
        return s

    def utc_timestamp(self, utc_dt: Optional[datetime.datetime] = None, ms: bool = False, micro: bool = False, milli: bool = False, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> int:
        return self.__micro_or_milli(self.datetime_to_timestamp(self.__utc_datetime(utc_dt, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), ms=ms), micro=micro, milli=milli)

    def local_timestamp(self, local_dt: Optional[datetime.datetime] = None, ms: bool = False, micro: bool = False, milli: bool = False, timezone: Optional[str] = None, years: int = 0, months: int = 0, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> int:
        return self.__micro_or_milli(self.datetime_to_timestamp(self.__local_datetime(local_dt, timezone=timezone, years=years, months=months, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks), ms=ms), micro=micro, milli=milli)

    def datetime_to_timestamp(self, dt: datetime.datetime, ms: bool = False) -> int:
        # http://stackoverflow.com/questions/26161156/python-converting-string-to-timestamp-with-microseconds
        # ``dt - epoch`` will raise ``TypeError: can't subtract offset-naive and offset-aware datetimes``
        # Total seconds from ``1970-01-01 00:00:00``(utc or local)
        # Different from definition of timestamp(时间戳是指格林威治时间1970年01月01日00时00分00秒(北京时间1970年01月01日08时00分00秒)起至现在的总秒数)
        stamp = self.structime_to_timestamp(dt.timetuple())
        if not ms:
            return stamp
        return stamp + dt.microsecond / self.SECOND_MICROSECOND

    def structime_to_timestamp(self, structime: time.struct_time) -> int:
        return int(time.mktime(structime))

    def seconds_to_microseconds(self, s: int) -> int:
        return self.__seconds_to_other(s, base=self.SECOND_MICROSECOND)

    def seconds_to_milliseconds(self, s: int) -> int:
        return self.__seconds_to_other(s, base=self.SECOND_MILLISECOND)

    # STRING ==> DATE

    def string_to_date(self, string: str, format: Optional[str] = None) -> Optional[datetime.date]:
        format = self.value_format(string, format)
        if not self.validate_string(string, format):
            return None
        return self.string_to_datetime(string, format).date()

    def string_to_utc_date(self, string: str, format: Optional[str] = None) -> Optional[datetime.date]:
        format = self.value_format(string, format)
        if not self.validate_string(string, format):
            return None
        return self.string_to_utc_datetime(string, format).date()

    def string_to_local_date(self, string: str, format: Optional[str] = None) -> Optional[datetime.date]:
        format = self.value_format(string, format)
        if not self.validate_string(string, format):
            return None
        return self.string_to_local_datetime(string, format).date()

    def utc_string_to_utc_date(self, utc_string: str, format: Optional[str] = None) -> Optional[datetime.date]:
        format = self.value_format(utc_string, format)
        if not self.validate_string(utc_string, format):
            return None
        return self.utc_string_to_utc_datetime(utc_string, format).date()

    def utc_string_to_local_date(self, utc_string: str, format: Optional[str] = None) -> Optional[datetime.date]:
        format = self.value_format(utc_string, format)
        if not self.validate_string(utc_string, format):
            return None
        return self.utc_string_to_local_datetime(utc_string, format).date()

    # STRING ==> DATETIME

    def string_to_datetime(self, string: str, format: Optional[str] = None) -> Optional[datetime.datetime]:
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return datetime.datetime.strptime(string, format)

    def string_to_utc_datetime(self, string: str, format: Optional[str] = None) -> Optional[datetime.datetime]:
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return self.to_utc_datetime(self.string_to_datetime(string, format))

    def string_to_local_datetime(self, string: str, format: Optional[str] = None) -> Optional[datetime.datetime]:
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return self.to_local_datetime(self.string_to_datetime(string, format)) - self.offset()

    def utc_string_to_utc_datetime(self, utc_string: str, format: Optional[str] = None) -> Optional[datetime.datetime]:
        format = self.format(format)
        if not self.validate_string(utc_string, format):
            return None
        return self.to_utc_datetime(self.string_to_datetime(utc_string, format)) + self.offset()

    def utc_string_to_local_datetime(self, utc_string: str, format: Optional[str] = None) -> Optional[datetime.datetime]:
        format = self.format(format)
        if not self.validate_string(utc_string, format):
            return None
        return self.to_local_datetime(self.string_to_datetime(utc_string, format))

    # STRING ==> TIMESTAMP

    def string_to_timestamp(self, string: str, format: Optional[str] = None, ms: bool = False) -> Optional[int]:
        return self.string_to_local_timestamp(string, format, ms=ms)

    def string_to_utc_timestamp(self, string: str, format: Optional[str] = None, ms: bool = False) -> Optional[int]:
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return self.datetime_to_timestamp(self.string_to_utc_datetime(string, format), ms=ms)

    def string_to_local_timestamp(self, string: str, format: Optional[str] = None, ms: bool = False) -> Optional[int]:
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return self.datetime_to_timestamp(self.string_to_local_datetime(string, format), ms=ms)

    # TIMESTAMP ==> DATETIME

    # local_stamp => utc_datetime - fromtimestamp + to_utc_datetime / utcfromtimestamp
    # local_stamp => local_datetime - fromtimestamp
    # utc_stamp => utc_datetime - fromtimestamp
    # utc_stamp => local_datetime - fromtimestamp + to_local_datetime
    def timestamp_to_datetime(self, stamp: int) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(stamp)

    def timestamp_to_utc_datetime(self, stamp: int) -> datetime.datetime:
        # return datetime.datetime.utcfromtimestamp(stamp)
        return self.to_utc_datetime(self.timestamp_to_datetime(stamp))

    def timestamp_to_local_datetime(self, stamp: int) -> datetime.datetime:
        return self.timestamp_to_datetime(stamp)

    def utc_timestamp_to_utc_datetime(self, stamp: int) -> datetime.datetime:
        # return self.make_aware(self.timestamp_to_datetime(stamp), timezone='UTC')
        return self.make_aware(self.timestamp_to_datetime(stamp), timezone=self.timezone('UTC'))

    def utc_timestamp_to_local_datetime(self, stamp: int) -> datetime.datetime:
        return self.to_local_datetime(self.timestamp_to_datetime(stamp))

    # TIMESTAMP ==> AGE

    # TIME_DELTA

    def timestamp_delta(self, stamp1: int, stamp2: int, interval: Optional[int] = None) -> Dict[str, Any]:
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

    def datetime_delta(self, dt1: datetime.datetime, dt2: datetime.datetime, interval: Optional[int] = None) -> Optional[Dict[str, Any]]:
        return self.timestamp_delta(self.datetime_to_timestamp(dt1), self.datetime_to_timestamp(dt2), interval)

    def string_delta(self, string1: str, string2: str, interval: Optional[int] = None, format: Optional[str] = None, format1: Optional[str] = None, format2: Optional[str] = None) -> Optional[Dict[str, Any]]:
        format = self.format(format)
        if (not self.validate_string(string1, format1 or format)) or (not self.validate_string(string2, format2 or format)):
            return None
        return self.timestamp_delta(self.string_to_timestamp(string1, format1 or format), self.string_to_timestamp(string2, format2 or format), interval)

    # TIME_COUNT_DOWN

    def timestamp_countdown(self, stamp: int, utc: bool = True) -> int:
        return abs(min((self.utc_timestamp() if utc else self.local_timestamp()) - stamp, 0))

    def datetime_countdown(self, dt: datetime.datetime) -> int:
        return self.timestamp_countdown(self.datetime_to_timestamp(self.to_utc_datetime(dt)))

    def string_countdown(self, string: str, format: Optional[str] = None) -> Optional[int]:
        format = self.format(format)
        if not self.validate_string(string, format):
            return None
        return self.timestamp_countdown(self.string_to_utc_timestamp(string, format))

    # MIDNIGHT

    def utc_datetime_midnight(self, utc_dt: Optional[datetime.datetime] = None) -> datetime.datetime:
        return (self.__utc_datetime(utc_dt)).replace(hour=0, minute=0, second=0, microsecond=0)

    def utc_seconds_since_midnight(self, utc_dt: Optional[datetime.datetime] = None, seconds_cast_func: Callable[[Any], T] = float) -> T:
        utc_dt = self.__utc_datetime(utc_dt)
        return seconds_cast_func(self.total_seconds(utc_dt - self.utc_datetime_midnight(utc_dt)))

    def local_datetime_midnight(self, local_dt: Optional[datetime.datetime] = None) -> datetime.datetime:
        return (self.__local_datetime(local_dt)).replace(hour=0, minute=0, second=0, microsecond=0)

    def local_seconds_since_midnight(self, local_dt: Optional[datetime.datetime] = None, seconds_cast_func: Callable[[Any], T] = float) -> T:
        local_dt = self.__local_datetime(local_dt)
        return seconds_cast_func(self.total_seconds(local_dt - self.local_datetime_midnight(local_dt)))

    def datetime_midnight(self, dt: Optional[datetime.datetime] = None, utc: bool = False) -> datetime.datetime:
        return self.utc_datetime_midnight(dt) if utc else self.local_datetime_midnight(dt)

    def seconds_since_midnight(self, dt: Optional[datetime.datetime] = None, utc: bool = False, seconds_cast_func: Callable[[Any], T] = float) -> T:
        return seconds_cast_func(self.utc_seconds_since_midnight(dt) if utc else self.local_seconds_since_midnight(dt))

    def seconds_until_midnight(self, dt: Optional[datetime.datetime] = None, utc: bool = False, seconds_cast_func: Callable[[Any], T] = float) -> T:
        return seconds_cast_func(86400 - self.seconds_since_midnight(dt=dt, utc=utc))

    # AWARE vs. NAIVE

    # By design, these four functions don't perform any checks on their arguments.
    # The caller should ensure that they don't receive an invalid value like None.

    def is_aware(self, value: datetime.datetime) -> bool:
        """
        Determine if a given datetime.datetime is aware.
        The concept is defined in Python's docs:
        https://docs.python.org/library/datetime.html#datetime.tzinfo
        Assuming value.tzinfo is either None or a proper datetime.tzinfo,
        value.utcoffset() implements the appropriate logic.
        """
        return value.utcoffset() is not None

    def is_naive(self, value: datetime.datetime) -> bool:
        """
        Determine if a given datetime.datetime is naive.
        The concept is defined in Python's docs:
        https://docs.python.org/library/datetime.html#datetime.tzinfo
        Assuming value.tzinfo is either None or a proper datetime.tzinfo,
        value.utcoffset() implements the appropriate logic.
        """
        return value.utcoffset() is None

    def make_aware(self, value: datetime.datetime, timezone: Optional[str] = None) -> datetime.datetime:
        """Make a naive datetime.datetime in a given time zone aware."""
        tzinfo = tz.gettz(self.timezone(timezone))
        # Check that we won't overwrite the timezone of an aware datetime.
        if self.is_aware(value):
            raise ValueError('make_aware expects a naive datetime, got %s' % value)
        # This may be wrong around DST changes!
        return value.replace(tzinfo=tzinfo)

    def make_naive(self, value: datetime.datetime, timezone: Optional[str] = None) -> datetime.datetime:
        """Make an aware datetime.datetime naive in a given time zone."""
        tzinfo = tz.gettz(self.timezone(timezone))
        # Emulate the behavior of astimezone() on Python < 3.6.
        if self.is_naive(value):
            raise ValueError('make_naive() cannot be applied to a naive datetime')
        return value.astimezone(tzinfo).replace(tzinfo=None)

    # PAST vs. FUTURE

    def is_past_time(self, value: Union[str, int, datetime.datetime], base_dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = True) -> Optional[bool]:
        base_dt = base_dt or self.basic_utc_datetime()

        if not value:
            return None

        if isinstance(value, datetime.datetime):
            return (value if utc else self.to_local_datetime(value)) < base_dt

        if isinstance(value, (str, bytes)):
            utc_dt = self.utc_string_to_utc_datetime(value, format=format) if utc else self.string_to_utc_datetime(value, format=format)
            return utc_dt and utc_dt < base_dt

        if isinstance(value, int):
            stamp = self.datetime_to_timestamp(base_dt if utc else self.to_local_datetime(base_dt), ms=True)
            return value < stamp

        return None

    def is_future_time(self, value: Union[str, int, datetime.datetime], base_dt: Optional[datetime.datetime] = None, format: Optional[str] = None, utc: bool = True) -> Optional[bool]:
        base_dt = base_dt or self.basic_utc_datetime()

        if not value:
            return None

        if isinstance(value, datetime.datetime):
            return (value if utc else self.to_local_datetime(value)) > base_dt

        if isinstance(value, (str, bytes)):
            utc_dt = self.utc_string_to_utc_datetime(value, format=format) if utc else self.string_to_utc_datetime(value, format=format)
            return utc_dt and utc_dt > base_dt

        if isinstance(value, int):
            stamp = self.datetime_to_timestamp(base_dt if utc else self.to_local_datetime(base_dt), ms=True)
            return value > stamp

        return None

    # YEAR/MONTH/DAY

    def year(self, dt: Optional[datetime.datetime] = None, utc: bool = False, timezone: Optional[str] = None, idx: int = 0) -> int:
        return self.__datetime(dt=self.several_time_coming(dt=dt, utc=utc, timezone=timezone, years=idx), utc=utc).year

    def month(self, dt: Optional[datetime.datetime] = None, utc: bool = False, timezone: Optional[str] = None, idx: int = 0) -> int:
        return self.__datetime(dt=self.several_time_coming(dt=dt, utc=utc, timezone=timezone, months=idx), utc=utc).month

    def day(self, dt: Optional[datetime.datetime] = None, utc: bool = False, timezone: Optional[str] = None, idx: int = 0) -> int:
        return self.__datetime(dt=self.several_time_coming(dt=dt, utc=utc, timezone=timezone, days=idx), utc=utc).day

    def days_of_year(self, year: Optional[int] = None, dt: Optional[datetime.datetime] = None, idx: int = 0) -> int:
        return 366 if calendar.isleap(year or self.year(dt, idx=idx)) else 365

    def days_of_month(self, year: Optional[int] = None, month: Optional[int] = None, dt: Optional[datetime.datetime] = None, idx: int = 0) -> int:
        return calendar.monthrange(year=(year or self.year(dt, idx=idx)), month=(month or self.month(dt, idx=idx)))[-1]

    # OTHER

    def total_seconds(self, td: datetime.timedelta, ms: bool = True) -> int:
        """Total seconds in the duration."""
        if not ms:
            return td.days * 86400 + td.seconds
        return ((td.days * 86400 + td.seconds) * self.SECOND_MICROSECOND + td.microseconds) / self.SECOND_MICROSECOND

    def date_range(self, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date], include_end: bool = False, format: Optional[str] = None, start_date_format: Optional[str] = None, end_date_format: Optional[str] = None, return_type: str = 'date', return_format: Optional[str] = None) -> Callable:
        if isinstance(start_date, str):
            start_date = self.string_to_date(start_date, start_date_format or format or self.DATE_FORMAT)
        if isinstance(end_date, str):
            end_date = self.string_to_date(end_date, end_date_format or format or self.DATE_FORMAT)
        if include_end:
            end_date = end_date + datetime.timedelta(1)
        if return_type in ['string', 'str']:
            for n in range(int((end_date - start_date).days)):
                yield self.datetime_to_string(start_date + datetime.timedelta(n), return_format or format or self.DATE_FORMAT)
        else:
            for n in range(int((end_date - start_date).days)):
                yield start_date + datetime.timedelta(n)

    def week_range(self, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date], format: Optional[str] = None, start_date_format: Optional[str] = None, end_date_format: Optional[str] = None, return_type: str = 'isoweek', return_format: Optional[str] = None) -> Callable:
        if isinstance(start_date, str):
            start_date = self.string_to_date(start_date, start_date_format or format or self.DATE_FORMAT)
        if isinstance(end_date, str):
            end_date = self.string_to_date(end_date, end_date_format or format or self.DATE_FORMAT)
        start_week = Week.withdate(start_date)
        end_week = Week.withdate(end_date)
        if return_type in ['string', 'str']:
            for n in range(int(end_week - start_week) + 1):
                current_week = start_week + n
                yield {
                    'week': current_week.isoformat(),
                    'start': self.datetime_to_string(current_week.monday(), return_format or format or self.DATE_FORMAT),
                    'end': self.datetime_to_string(current_week.sunday(), return_format or format or self.DATE_FORMAT),
                }
        else:
            for n in range(int(end_week - start_week) + 1):
                yield start_week + n

    def month_range(self, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date], format: Optional[str] = None, start_date_format: Optional[str] = None, end_date_format: Optional[str] = None, return_type: str = 'date', return_format: Optional[str] = None) -> Callable:
        if isinstance(start_date, str):
            start_date = self.string_to_date(start_date, start_date_format or format or self.DATE_FORMAT)
        if isinstance(end_date, str):
            end_date = self.string_to_date(end_date, end_date_format or format or self.DATE_FORMAT)
        start_month = Month.from_date(start_date)
        end_month = Month.from_date(end_date)
        if return_type in ['string', 'str']:
            for n in range(int(end_month - start_month) + 1):
                current_month = start_month + n
                yield {
                    'month': str(current_month),
                    'start': self.datetime_to_string(current_month.start_date, return_format or format or self.DATE_FORMAT),
                    'end': self.datetime_to_string(current_month.end_date, return_format or format or self.DATE_FORMAT),
                }
        else:
            for n in range(int(end_month - start_month) + 1):
                yield start_month + n

    def quarter_range(self, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date], format: Optional[str] = None, start_date_format: Optional[str] = None, end_date_format: Optional[str] = None, return_type: str = 'date', return_format: Optional[str] = None) -> Callable:
        if isinstance(start_date, str):
            start_date = self.string_to_date(start_date, start_date_format or format or self.DATE_FORMAT)
        if isinstance(end_date, str):
            end_date = self.string_to_date(end_date, end_date_format or format or self.DATE_FORMAT)
        start_quarter = Quarter.from_date(start_date)
        end_quarter = Quarter.from_date(end_date)
        if return_type in ['string', 'str']:
            for n in range(int(end_quarter - start_quarter) + 1):
                current_quarter = start_quarter + n
                yield {
                    'quarter': current_quarter.isoformat(),
                    'start': self.datetime_to_string(current_quarter.start_date, return_format or format or self.DATE_FORMAT),
                    'end': self.datetime_to_string(current_quarter.end_date, return_format or format or self.DATE_FORMAT),
                }
        else:
            for n in range(int(end_quarter - start_quarter) + 1):
                yield start_quarter + n

    daterange = date_range
    weekrange = week_range
    monthrange = month_range
    quarterrange = quarter_range

    def isoweekdaycount(self, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date], isoweekday: int = 7, format: Optional[str] = None, start_date_format: Optional[str] = None, end_date_format: Optional[str] = None) -> int:
        if isinstance(start_date, str):
            start_date = self.string_to_date(start_date, start_date_format or format or self.DATE_FORMAT)
        if isinstance(end_date, str):
            end_date = self.string_to_date(end_date, end_date_format or format or self.DATE_FORMAT)
        weeks = self.datetime_delta(start_date, end_date).get('weeks')
        # datetime.datetime.now().isoweekday()  # 返回1-7，代表周一到周日，当前时间所在本周第几天
        # datetime.datetime.now().weekday()  # 返回的0-6，代表周一到周日
        # 标准格式 %w 中，1-6表示周一到周六，0代表周日
        start_isoweekday = start_date.isoweekday()
        end_isoweekday = end_date.isoweekday()
        if end_isoweekday >= start_isoweekday:
            if start_isoweekday <= isoweekday <= end_isoweekday:
                weeks += 1
        else:
            if start_isoweekday <= isoweekday or end_isoweekday >= isoweekday:
                weeks += 1
        return weeks


TC = tc = TimeConvert = TimeConvertTools()

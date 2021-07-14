# -*- coding: utf-8 -*-

import datetime

import pytz

from TimeConvert import TimeConvert as tc


class TestTimeConvertCommands(object):

    # Variable

    def test_time_zone(self):
        assert tc.timezone() == tc.TIME_ZONE
        timezone = 'UTC'
        tc.__init__(timezone=timezone)
        assert tc.TIME_ZONE == timezone
        assert tc.timezone() == timezone

    def test_time_format(self):
        assert tc.format() == tc.TIME_FORMAT
        timeformat = '%Y%m%d%H%M%S'
        tc.__init__(format=timeformat)
        assert tc.TIME_FORMAT == timeformat
        assert tc.format() == timeformat
        tc.__init__(format=tc.DATETIME_FORMAT)

    # OFFSET

    def test_offset(self):
        assert tc.offset() == datetime.timedelta(0, 28800)

    # VALIDATE

    def test_validate_string(self):
        assert tc.validate_string('1988-06-15 08:08:08', '%Y-%m-%d %H:%M:%S')
        assert not tc.validate_string('19880615080808', '%Y-%m-%d %H:%M:%S')

    # REPLACE

    def test_remove_microsecond(self):
        dt = tc.remove_microsecond(tc.utc_datetime())
        assert dt.microsecond == 0

    # DATE

    def test_utc_date(self):
        assert isinstance(tc.local_date(), datetime.date)

    def test_local_date(self):
        assert tc.local_date() == datetime.datetime.date(datetime.datetime.now())

    # DATETIME

    def test_utc_datetime(self):
        dt = tc.utc_datetime()
        assert dt.tzinfo == pytz.utc
        dt = tc.utc_datetime(ms=False)
        assert dt.microsecond == 0

    def test_local_datetime(self):
        dt = tc.local_datetime()
        assert str(dt.tzinfo) == tc.TIME_ZONE
        dt = tc.local_datetime(ms=False)
        assert dt.microsecond == 0

    def test_is_utc_datetime(self):
        assert tc.is_utc_datetime(tc.utc_datetime())
        assert not tc.is_utc_datetime(tc.local_datetime())

    def test_is_local_datetime(self):
        assert tc.is_local_datetime(tc.local_datetime())
        assert tc.is_local_datetime(tc.local_datetime(), local_tz=tc.TIME_ZONE)
        assert not tc.is_local_datetime(tc.utc_datetime())

    def test_to_utc_datetime(self):
        assert tc.is_utc_datetime(tc.to_utc_datetime(tc.utc_datetime()))
        assert tc.is_utc_datetime(tc.to_utc_datetime(tc.local_datetime()))

    def test_to_local_datetime(self):
        assert tc.is_local_datetime(tc.to_local_datetime(tc.utc_datetime()))
        assert tc.is_local_datetime(tc.to_local_datetime(tc.local_datetime()))

    def test_yesterday_utc_datetime(self):
        assert isinstance(tc.yesterday_utc_datetime(), datetime.datetime)

    def test_tomorrow_utc_datetime(self):
        assert isinstance(tc.tomorrow_utc_datetime(), datetime.datetime)

    def test_yesterday_local_datetime(self):
        assert isinstance(tc.yesterday_local_datetime(), datetime.datetime)

    def test_tomorrow_local_datetime(self):
        assert isinstance(tc.tomorrow_local_datetime(), datetime.datetime)

    def test_several_days_ago(self):
        assert isinstance(tc.several_days_ago(days=1), datetime.datetime)

    def test_several_days_coming(self):
        assert isinstance(tc.several_days_coming(days=1), datetime.datetime)

    def test_several_time_ago(self):
        assert isinstance(tc.several_time_ago(days=1), datetime.datetime)

    def test_several_time_coming(self):
        assert isinstance(tc.several_time_coming(days=1), datetime.datetime)

    # STRING

    def test_utc_string(self):
        assert tc.validate_string(tc.utc_string())

    def test_local_string(self):
        assert tc.validate_string(tc.local_string())

    def test_utc_datetime_string(self):
        assert tc.validate_string(tc.utc_datetime_string(), tc.DATETIME_FORMAT)

    def test_local_datetime_string(self):
        assert tc.validate_string(tc.local_datetime_string(), tc.DATETIME_FORMAT)

    def test_utc_date_string(self):
        assert tc.validate_string(tc.utc_date_string(), tc.DATE_FORMAT)

    def test_local_date_string(self):
        assert tc.validate_string(tc.local_date_string(), tc.DATE_FORMAT)

    def test_utc_week_string(self):
        assert tc.validate_string(tc.utc_week_string(), tc.WEEK_FORMAT)

    def test_local_week_string(self):
        assert tc.validate_string(tc.local_week_string(), tc.WEEK_FORMAT)

    def test_datetime_to_string(self):
        assert tc.validate_string(tc.datetime_to_string(tc.utc_datetime()))

    def test_datetime_to_unicode_string(self):
        assert tc.datetime_to_unicode_string(tc.utc_datetime(), format=u'%Y年%m月%d日 %H时%M分%S秒')

    # TIMESTAMP

    def test_utc_timestamp(self):
        assert isinstance(tc.utc_timestamp(), int)
        assert isinstance(tc.utc_timestamp(ms=True), float)

    def test_local_timestamp(self):
        assert isinstance(tc.local_timestamp(), int)
        assert isinstance(tc.local_timestamp(ms=True), float)

    def test_datetime_to_timestamp(self):
        dt = tc.utc_datetime()
        assert isinstance(tc.datetime_to_timestamp(dt=dt), int)
        assert isinstance(tc.datetime_to_timestamp(dt=dt, ms=True), float)

    # STRING ==> DATETIME

    def test_string_to_datetime(self):
        assert tc.is_local_datetime(tc.string_to_datetime('1988-06-15 08:08:08'), local_tz=-1)

    def test_string_to_utc_datetime(self):
        assert tc.is_utc_datetime(tc.string_to_utc_datetime('1988-06-15 08:08:08'))

    def test_string_to_local_datetime(self):
        assert tc.is_local_datetime(tc.string_to_local_datetime('1988-06-15 08:08:08'))

    def test_utc_string_to_utc_datetime(self):
        assert tc.is_utc_datetime(tc.utc_string_to_utc_datetime('1988-06-15 08:08:08'))

    def test_utc_string_to_local_datetime(self):
        assert tc.is_local_datetime(tc.utc_string_to_local_datetime('1988-06-15 08:08:08'))

    # PAST vs. FUTURE

    def test_is_past_time(self):
        assert not tc.is_past_time('')
        # Datetime
        assert tc.is_past_time(tc.utc_datetime())
        assert tc.is_past_time(tc.local_datetime(), utc=False)
        # String
        assert tc.is_past_time(tc.utc_string())
        assert tc.is_past_time(tc.local_string(), utc=False)
        assert tc.is_past_time(tc.utc_string(format='%Y-%m-%dT%H:%M:%SZ'), format='%Y-%m-%dT%H:%M:%SZ')
        # Stamp
        assert tc.is_past_time(tc.utc_timestamp())
        assert tc.is_past_time(tc.local_timestamp(), utc=False)
        # Base_dt
        assert not tc.is_past_time(tc.utc_datetime(), base_dt=tc.several_time_ago(hours=1))
        assert tc.is_past_time(tc.several_time_ago(hours=2), base_dt=tc.several_time_ago(hours=1))

    def test_is_future_time(self):
        assert not tc.is_future_time('')
        # Datetime
        assert tc.is_future_time(tc.utc_datetime(), base_dt=tc.several_time_ago(hours=1))
        assert tc.is_future_time(tc.local_datetime(), base_dt=tc.several_time_ago(hours=1), utc=False)
        # String
        assert tc.is_future_time(tc.utc_string(), base_dt=tc.several_time_ago(hours=1))
        assert tc.is_future_time(tc.local_string(), base_dt=tc.several_time_ago(hours=1), utc=False)
        assert tc.is_future_time(tc.utc_string(format='%Y-%m-%dT%H:%M:%SZ'), base_dt=tc.several_time_ago(hours=1), format='%Y-%m-%dT%H:%M:%SZ')
        # Stamp
        assert tc.is_future_time(tc.utc_timestamp(), base_dt=tc.several_time_ago(hours=1))
        assert tc.is_future_time(tc.local_timestamp(), base_dt=tc.several_time_ago(hours=1), utc=False)
        # Base_dt
        assert tc.is_future_time(tc.utc_datetime(), base_dt=tc.several_time_ago(hours=1))
        assert not tc.is_future_time(tc.several_time_ago(hours=2), base_dt=tc.several_time_ago(hours=1))

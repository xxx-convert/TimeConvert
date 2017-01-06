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

    # OFFSET

    def test_offset(self):
        assert tc.offset() == datetime.timedelta(0, 28800)

    # VALIDATE

    def test_validate_string(self):
        assert tc.validate_string('1988-06-15 12:12:12', '%Y-%m-%d %H:%M:%S')
        assert not tc.validate_string('19880615121212', '%Y-%m-%d %H:%M:%S')

    # REPLACE

    def test_remove_microsecond(self):
        dt = tc.remove_microsecond(tc.utc_datetime())
        assert dt.microsecond == 0

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
        pass

    def test_tomorrow_utc_datetime(self):
        pass

    def test_yesterday_local_datetime(self):
        pass

    def test_tomorrow_local_datetime(self):
        pass

    def test_several_days_ago(self):
        pass

    def test_several_days_coming(self):
        pass

    def test_several_time_ago(self):
        pass

    def test_several_time_coming(self):
        pass

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

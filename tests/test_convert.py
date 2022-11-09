# -*- coding: utf-8 -*-

import datetime
import types

import pytest
from dateutil.tz import tz

from TimeConvert import ISOWeek, Month, Quarter
from TimeConvert import TimeConvert as tc
from TimeConvert import Week


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

    def test_timezone(self):
        assert tc.timezone() == tc.TIME_ZONE
        assert tc.timezone(timezone=tc.TIME_ZONE) == tc.TIME_ZONE

    def test_format(self):
        assert tc.format() == tc.DATETIME_FORMAT
        assert tc.format(format=tc.DATETIME_FORMAT) == tc.DATETIME_FORMAT

    def test_date_format(self):
        assert tc.date_format() == tc.DATE_FORMAT
        assert tc.date_format(format=tc.DATE_FORMAT) == tc.DATE_FORMAT

    def test_value_format(self):
        assert tc.value_format(format=tc.DATETIME_FORMAT) == tc.DATETIME_FORMAT
        assert tc.value_format(format=tc.DATE_FORMAT) == tc.DATE_FORMAT
        assert tc.value_format('2017-12-08 15:27:00') == tc.DATETIME_FORMAT
        assert tc.value_format('2017-12-08') == tc.DATE_FORMAT

    # OFFSET

    def test_offset(self):
        assert tc.offset() == datetime.timedelta(0, 28800)

    # VALIDATE

    def test_validate_string(self):
        assert tc.validate_string('2017-12-08 15:27:00', '%Y-%m-%d %H:%M:%S')
        assert not tc.validate_string('19880615080808', '%Y-%m-%d %H:%M:%S')

    # REPLACE

    def test_remove_microsecond(self):
        dt = tc.remove_microsecond(tc.utc_datetime())
        assert dt.microsecond == 0

    # DATETIME

    def test_utc_datetime(self):
        dt = tc.utc_datetime()
        assert dt.tzinfo == tz.UTC
        dt = tc.utc_datetime(ms=False)
        assert dt.microsecond == 0

    def test_local_datetime(self):
        dt = tc.local_datetime()
        assert dt.tzinfo == tz.gettz(tc.TIME_ZONE)
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

    # DATE

    def test_utc_date(self):
        assert isinstance(tc.utc_date(), datetime.date)
        assert tc.utc_date(datetime.datetime(2017, 12, 8, 15, 27, 0)) == datetime.date(2017, 12, 8)
        assert tc.utc_date(datetime.date(2017, 12, 8)) == datetime.date(2017, 12, 8)
        assert tc.utc_date() == datetime.datetime.date(datetime.datetime.utcnow())

    def test_local_date(self):
        assert isinstance(tc.local_date(), datetime.date)
        assert tc.local_date(datetime.datetime(2017, 12, 8, 15, 27, 0)) == datetime.date(2017, 12, 8)
        assert tc.local_date(datetime.date(2017, 12, 8)) == datetime.date(2017, 12, 8)
        assert tc.local_date() == datetime.datetime.date(datetime.datetime.now())

    def test_datetime_to_date(self):
        assert tc.to_date(datetime.datetime(2017, 12, 8, 15, 27, 0)) == datetime.date(2017, 12, 8)

    def test_to_date(self):
        assert tc.to_date('2017-12-08 15:27:00', format=tc.DATETIME_FORMAT) == datetime.date(2017, 12, 8)
        assert tc.to_date('2017-12-08') == datetime.date(2017, 12, 8)
        assert tc.to_date(datetime.datetime(2017, 12, 8, 15, 27, 0)) == datetime.date(2017, 12, 8)
        assert tc.to_date(datetime.date(2017, 12, 8)) == datetime.date(2017, 12, 8)
        assert tc.to_date('2017-12-08 15:27:00', idx=-1) == datetime.date(2017, 12, 7)
        assert tc.to_date('2017-12-08 15:27:00', idx=1) == datetime.date(2017, 12, 9)

    def test_is_the_same_day(self):
        assert tc.is_the_same_day(datetime.datetime(2017, 12, 8, 15, 27, 0), '2017-12-08 15:27:00')
        assert tc.is_the_same_day(datetime.datetime(2017, 12, 8, 15, 27, 0), '2017-12-08')
        assert tc.is_the_same_day(datetime.datetime(2017, 12, 8, 15, 27, 0), datetime.date(2017, 12, 8))
        assert tc.is_the_same_day(datetime.datetime(2017, 12, 8, 15, 27, 0), datetime.datetime(2017, 12, 8, 15, 27, 0))

    # YEAR WEEK

    def test_utc_yearweek(self):
        assert isinstance(tc.utc_yearweek(), (Week, ISOWeek))
        assert tc.utc_yearweek(datetime.date(2017, 12, 31), mode=0) == Week(2017, 53)
        assert tc.utc_yearweek(datetime.date(2017, 12, 31), mode=3) == ISOWeek(2017, 52)
        assert tc.utc_yearweek(datetime.date(2017, 12, 31), mode=5) == Week(2017, 52)

    def test_utc_isoyearweek(self):
        assert isinstance(tc.utc_isoyearweek(), ISOWeek)
        assert tc.utc_isoyearweek(datetime.date(2017, 12, 31)) == ISOWeek(2017, 52)

    def test_local_yearweek(self):
        assert isinstance(tc.local_yearweek(), (Week, ISOWeek))
        assert tc.local_yearweek(datetime.date(2017, 12, 31), mode=0) == Week(2017, 53)
        assert tc.local_yearweek(datetime.date(2017, 12, 31), mode=3) == ISOWeek(2017, 52)
        assert tc.local_yearweek(datetime.date(2017, 12, 31), mode=5) == Week(2017, 52)

    def test_local_isoyearweek(self):
        assert isinstance(tc.local_isoyearweek(), ISOWeek)
        assert tc.local_isoyearweek(datetime.date(2017, 12, 31)) == ISOWeek(2017, 52)

    # WEEK

    def test_utc_week(self):
        assert isinstance(tc.utc_week(), int)
        assert tc.utc_week(datetime.date(2017, 12, 31), mode=0) == 53
        assert tc.utc_week(datetime.date(2017, 12, 31), mode=3) == 52
        assert tc.utc_week(datetime.date(2017, 12, 31), mode=5) == 52

    def test_utc_isoweek(self):
        assert isinstance(tc.utc_isoweek(), int)
        assert tc.utc_isoweek(datetime.date(2017, 12, 31)) == 52

    def test_local_week(self):
        assert isinstance(tc.local_week(), int)
        assert tc.local_week(datetime.date(2017, 12, 31), mode=0) == 53
        assert tc.local_week(datetime.date(2017, 12, 31), mode=3) == 52
        assert tc.local_week(datetime.date(2017, 12, 31), mode=5) == 52

    def test_local_isoweek(self):
        assert isinstance(tc.local_isoweek(), int)
        assert tc.local_isoweek(datetime.date(2017, 12, 31)) == 52

    def test_to_week(self):
        with pytest.raises(ValueError):
            tc.to_week('2017-12-08 15:27:00', mode=0)

    def test_to_isoweek(self):
        assert tc.to_isoweek('2017-12-08 15:27:00') == ISOWeek(2017, 49)
        assert tc.to_isoweek('2017-12-08') == ISOWeek(2017, 49)
        assert tc.to_isoweek(datetime.datetime(2017, 12, 8, 15, 27, 0)) == ISOWeek(2017, 49)
        assert tc.to_isoweek(datetime.date(2017, 12, 8)) == ISOWeek(2017, 49)
        assert tc.to_isoweek('2017-12-08 15:27:00', idx=-1) == ISOWeek(2017, 48)
        assert tc.to_isoweek('2017-12-08 15:27:00', idx=1) == ISOWeek(2017, 50)

    def test_weekdelta(self):
        assert tc.weekdelta('2017-12-31 15:27:00', '2017-12-08 15:27:00') == 3

    def test_isoweekdelta(self):
        assert tc.isoweekdelta('2017-12-31 15:27:00', '2017-12-08 15:27:00') == 3

    # STRING

    # DATETIME_STRING
    def test_datetime_to_unicode_string(self):
        assert tc.datetime_to_unicode_string(tc.utc_datetime(), format=u'%Y年%m月%d日 %H时%M分%S秒')

    def test_datetime_to_string(self):
        assert tc.validate_string(tc.datetime_to_string(tc.utc_datetime()))

    def test_utc_string(self):
        assert tc.validate_string(tc.utc_string())

    def test_local_string(self):
        assert tc.validate_string(tc.local_string())

    def test_utc_datetime_string(self):
        assert tc.validate_string(tc.utc_datetime_string(), tc.DATETIME_FORMAT)

    def test_local_datetime_string(self):
        assert tc.validate_string(tc.local_datetime_string(), tc.DATETIME_FORMAT)

    # DATE_STRING
    def test_utc_date_string(self):
        assert tc.validate_string(tc.utc_date_string(), tc.DATE_FORMAT)

    def test_local_date_string(self):
        assert tc.validate_string(tc.local_date_string(), tc.DATE_FORMAT)

    # YEAR_WEEK_STRING
    def test_utc_yearweek_string(self):
        assert isinstance(tc.utc_yearweek_string(), str)
        assert tc.utc_yearweek_string(datetime.date(2017, 12, 31), mode=0) == '2017W53'
        assert tc.utc_yearweek_string(datetime.date(2017, 12, 31), mode=3) == '2017W52'
        assert tc.utc_yearweek_string(datetime.date(2017, 12, 31), mode=5) == '2017W52'

    def test_local_yearweek_string(self):
        assert isinstance(tc.local_yearweek_string(), str)
        assert tc.local_yearweek_string(datetime.date(2017, 12, 31), mode=0) == '2017W53'
        assert tc.local_yearweek_string(datetime.date(2017, 12, 31), mode=3) == '2017W52'
        assert tc.local_yearweek_string(datetime.date(2017, 12, 31), mode=5) == '2017W52'

    # WEEK_STRING
    def test_utc_week_string(self):
        assert isinstance(tc.utc_week_string(), str)

    def test_local_week_string(self):
        assert isinstance(tc.local_week_string(), str)

    # TIMESTAMP

    def test_utc_timestamp(self):
        assert isinstance(tc.utc_timestamp(), int)
        assert isinstance(tc.utc_timestamp(ms=True), float)
        assert isinstance(tc.utc_timestamp(days=1), int)
        assert isinstance(tc.utc_timestamp(ms=True, days=1), float)

    def test_local_timestamp(self):
        assert isinstance(tc.local_timestamp(), int)
        assert isinstance(tc.local_timestamp(ms=True), float)
        assert isinstance(tc.local_timestamp(days=1), int)
        assert isinstance(tc.local_timestamp(ms=True, days=1), float)

    def test_datetime_to_timestamp(self):
        dt = tc.utc_datetime()
        assert isinstance(tc.datetime_to_timestamp(dt=dt), int)
        assert isinstance(tc.datetime_to_timestamp(dt=dt, ms=True), float)

    # STRING ==> DATE

    def test_string_to_date(self):
        assert tc.string_to_date('2017-12-08') == datetime.date(2017, 12, 8)
        assert tc.string_to_date('2017-12-08 15:27:00') == datetime.date(2017, 12, 8)
        assert tc.string_to_date('2017-12-08 15:27:00', format=tc.DATETIME_FORMAT) == datetime.date(2017, 12, 8)

    def test_string_to_utc_date(self):
        assert tc.string_to_utc_date('2017-12-08') == datetime.date(2017, 12, 7)
        assert tc.string_to_utc_date('2017-12-08 15:27:00') == datetime.date(2017, 12, 8)
        assert tc.string_to_utc_date('2017-12-08 15:27:00', format=tc.DATETIME_FORMAT) == datetime.date(2017, 12, 8)

    def test_string_to_local_date(self):
        assert tc.string_to_local_date('2017-12-08') == datetime.date(2017, 12, 8)
        assert tc.string_to_local_date('2017-12-08 15:27:00') == datetime.date(2017, 12, 8)
        assert tc.string_to_local_date('2017-12-08 15:27:00', format=tc.DATETIME_FORMAT) == datetime.date(2017, 12, 8)

    def test_utc_string_to_utc_date(self):
        assert tc.utc_string_to_utc_date('2017-12-08') == datetime.date(2017, 12, 8)
        assert tc.utc_string_to_utc_date('2017-12-08 15:27:00') == datetime.date(2017, 12, 8)
        assert tc.utc_string_to_utc_date('2017-12-08 15:27:00', format=tc.DATETIME_FORMAT) == datetime.date(2017, 12, 8)

    def test_utc_string_to_local_date(self):
        assert tc.utc_string_to_local_date('2017-12-08') == datetime.date(2017, 12, 8)
        assert tc.utc_string_to_local_date('2017-12-08 15:27:00') == datetime.date(2017, 12, 8)
        assert tc.utc_string_to_local_date('2017-12-08 15:27:00', format=tc.DATETIME_FORMAT) == datetime.date(2017, 12, 8)

    # STRING ==> DATETIME

    def test_string_to_datetime(self):
        dt = tc.string_to_datetime('2017-12-08 15:27:00')
        assert dt == datetime.datetime(2017, 12, 8, 15, 27, 0)
        assert tc.is_local_datetime(dt, local_tz=-1)

    def test_string_to_utc_datetime(self):
        dt = tc.string_to_utc_datetime('2017-12-08 15:27:00')
        assert dt == datetime.datetime(2017, 12, 8, 7, 27, 0, tzinfo=tz.UTC)
        assert tc.is_utc_datetime(dt)

    def test_string_to_local_datetime(self):
        dt = tc.string_to_local_datetime('2017-12-08 15:27:00')
        assert tc.is_local_datetime(dt)

    def test_utc_string_to_utc_datetime(self):
        dt = tc.utc_string_to_utc_datetime('2017-12-08 15:27:00')
        assert dt == datetime.datetime(2017, 12, 8, 15, 27, 0, tzinfo=tz.UTC)
        assert tc.is_utc_datetime(dt)

    def test_utc_string_to_local_datetime(self):
        dt = tc.utc_string_to_local_datetime('2017-12-08 15:27:00')
        assert tc.is_local_datetime(dt)

    # TIME_DELTA

    def test_timestamp_delta(self):
        delta = tc.timestamp_delta(1514705220, 1512718020)
        assert isinstance(delta, dict)
        assert delta['total_seconds'] == 1987200

    def test_datetime_delta(self):
        delta = tc.datetime_delta(datetime.datetime(2017, 12, 31, 15, 27, 0), datetime.datetime(2017, 12, 8, 15, 27, 0))
        assert isinstance(delta, dict)
        assert delta['total_seconds'] == 1987200

    def test_date_delta(self):
        delta = tc.date_delta(datetime.date(2017, 12, 31), datetime.date(2017, 12, 8))
        assert isinstance(delta, dict)
        assert delta['total_seconds'] == 1987200

    def test_string_delta(self):
        delta = tc.string_delta('2017-12-31 15:27:00', '2017-12-08 15:27:00')
        assert isinstance(delta, dict)
        assert delta['total_seconds'] == 1987200

    def test_delta(self):
        delta = tc.timestamp_delta(1514705220, 1512718020)
        assert isinstance(delta, dict)
        assert delta['total_seconds'] == 1987200

        delta = tc.delta(datetime.datetime(2017, 12, 31, 15, 27, 0), datetime.datetime(2017, 12, 8, 15, 27, 0))
        assert isinstance(delta, dict)
        assert delta['total_seconds'] == 1987200

        delta = tc.delta(datetime.date(2017, 12, 31), datetime.date(2017, 12, 8))
        assert isinstance(delta, dict)
        assert delta['total_seconds'] == 1987200

        delta = tc.delta('2017-12-31 15:27:00', '2017-12-08 15:27:00')
        assert isinstance(delta, dict)
        assert delta['total_seconds'] == 1987200

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

    # OTHER

    def test_date_range(self):
        dates = tc.date_range('2017-12-08', '2017-12-31')
        assert isinstance(dates, types.GeneratorType)
        dates = [date for date in dates]
        assert isinstance(dates[0], datetime.date)
        assert dates[0] == datetime.date(2017, 12, 8)
        assert dates[-1] == datetime.date(2017, 12, 30)
        assert len(dates) == 23

        dates = tc.date_range('2017-12-08', '2017-12-31', include_end=True)
        dates = [date for date in dates]
        assert dates[-1] == datetime.date(2017, 12, 31)
        assert len(dates) == 24

        dates = tc.date_range('2017-12-08', '2017-12-31', include_end=True, return_type='string')
        dates = [date for date in dates]
        assert dates[-1] == '2017-12-31'

        dates = tc.date_range('2017-12-08', '2017-12-31', include_end=True, return_type='str', return_format='%Y%m%d')
        dates = [date for date in dates]
        assert dates[-1] == '20171231'

        dates = tc.date_range('20171208', '20171231', include_end=True, format='%Y%m%d', return_type='str')
        dates = [date for date in dates]
        assert dates[-1] == '20171231'

    def test_week_range(self):
        weeks = tc.week_range('2017-12-08', '2017-12-31')
        assert isinstance(weeks, types.GeneratorType)
        weeks = [week for week in weeks]
        assert isinstance(weeks[0], ISOWeek)
        assert weeks[0] == ISOWeek(2017, 49)
        assert weeks[-1] == ISOWeek(2017, 52)
        assert len(weeks) == 4

        weeks = tc.week_range('2017-12-08', '2017-12-31', return_type='string')
        weeks = [week for week in weeks]
        assert weeks[-1]['week'] == '2017W52'
        assert weeks[-1]['start'] == '2017-12-25'
        assert weeks[-1]['end'] == '2017-12-31'

        weeks = tc.week_range('2017-12-08', '2017-12-31', return_type='str', return_format='%Y%m%d')
        weeks = [week for week in weeks]
        assert weeks[-1]['week'] == '2017W52'
        assert weeks[-1]['start'] == '20171225'
        assert weeks[-1]['end'] == '20171231'

        weeks = tc.week_range('20171208', '20171231', format='%Y%m%d', return_type='str')
        weeks = [week for week in weeks]
        assert weeks[-1]['week'] == '2017W52'
        assert weeks[-1]['start'] == '20171225'
        assert weeks[-1]['end'] == '20171231'

    def test_month_range(self):
        months = tc.month_range('2017-12-08', '2017-12-31')
        assert isinstance(months, types.GeneratorType)
        months = [month for month in months]
        assert isinstance(months[0], Month)
        assert months[0] == Month(2017, 12)
        assert months[-1] == Month(2017, 12)
        assert len(months) == 1

        months = tc.month_range('2017-12-08', '2017-12-31', return_type='string')
        months = [month for month in months]
        assert months[-1]['month'] == '2017-12'
        assert months[-1]['start'] == '2017-12-01'
        assert months[-1]['end'] == '2017-12-31'

        months = tc.month_range('2017-12-08', '2017-12-31', return_type='str', return_format='%Y%m%d')
        months = [month for month in months]
        assert months[-1]['month'] == '2017-12'
        assert months[-1]['start'] == '20171201'
        assert months[-1]['end'] == '20171231'

        months = tc.month_range('20171208', '20171231', format='%Y%m%d', return_type='str')
        months = [month for month in months]
        assert months[-1]['month'] == '2017-12'
        assert months[-1]['start'] == '20171201'
        assert months[-1]['end'] == '20171231'

    def test_quarter_range(self):
        quarters = tc.quarter_range('2017-12-08', '2017-12-31')
        assert isinstance(quarters, types.GeneratorType)
        quarters = [quarter for quarter in quarters]
        assert isinstance(quarters[0], Quarter)
        assert quarters[0] == Quarter(2017, 4)
        assert quarters[-1] == Quarter(2017, 4)
        assert len(quarters) == 1

        quarters = tc.quarter_range('2017-12-08', '2017-12-31', return_type='string')
        quarters = [quarter for quarter in quarters]
        assert quarters[-1]['quarter'] == '2017Q4'
        assert quarters[-1]['start'] == '2017-10-01'
        assert quarters[-1]['end'] == '2017-12-31'

        quarters = tc.quarter_range('2017-12-08', '2017-12-31', return_type='str', return_format='%Y%m%d')
        quarters = [quarter for quarter in quarters]
        assert quarters[-1]['quarter'] == '2017Q4'
        assert quarters[-1]['start'] == '20171001'
        assert quarters[-1]['end'] == '20171231'

        quarters = tc.quarter_range('20171208', '20171231', format='%Y%m%d', return_type='str')
        quarters = [quarter for quarter in quarters]
        assert quarters[-1]['quarter'] == '2017Q4'
        assert quarters[-1]['start'] == '20171001'
        assert quarters[-1]['end'] == '20171231'

    def test_isoweekdaycount(self):
        assert tc.isoweekdaycount('2017-12-08', '2017-12-31') == 4
        assert tc.isoweekdaycount('2017-12-06', '2017-12-06', 3) == 1
        assert tc.isoweekdaycount('2017-12-08', '2017-12-31', 3) == 3
        assert tc.isoweekdaycount('2017-12-08', '2018-01-03', 3) == 4
        assert tc.isoweekdaycount('2017-12-06', '2018-01-03', 3) == 5

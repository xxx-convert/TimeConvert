# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime

from TimeConvert import TimeConvert as tc


TIME_FORMAT, TIME_ZONE = tc.TIME_FORMAT, tc.TIME_ZONE


def main():

    # Variable

    print(">> tc.TIME_ZONE")
    print("    Exec: {}".format("tc.TIME_ZONE"))
    print("    Result: {}".format(tc.TIME_ZONE))
    print()
    print(">> tc.TIME_FORM")
    print("    Exec: {}".format("tc.TIME_FORMAT"))
    print("    Result: {}".format(tc.TIME_FORMAT))
    print()

    # DATETIME

    print(">> utc_datetime()")
    print("    Exec: {}".format("tc.utc_datetime()"))
    print("    Result: {}".format(tc.utc_datetime()))
    print()
    print(">> local_datetime()")
    print("    Exec: {}".format("tc.local_datetime()"))
    print("    Result: {}".format(tc.local_datetime()))
    print()
    print(">> to_utc_datetime(local_dt, timezone=TIME_ZONE)")
    print("    Exec: {}".format("tc.to_utc_datetime(datetime.datetime.now(), timezone=TIME_ZONE)"))
    print("    Result: {}".format(tc.to_utc_datetime(datetime.datetime.now(), timezone=TIME_ZONE)))
    print("    Exec: {}".format("tc.to_utc_datetime(tc.local_datetime(), timezone=TIME_ZONE)"))
    print("    Result: {}".format(tc.to_utc_datetime(tc.local_datetime(), timezone=TIME_ZONE)))
    print("    Exec: {}".format("tc.to_utc_datetime(tc.utc_datetime(), timezone=TIME_ZONE)"))
    print("    Result: {}".format(tc.to_utc_datetime(tc.utc_datetime(), timezone=TIME_ZONE)))
    print("    Exec: {}".format("tc.to_utc_datetime(tc.make_naive(tc.utc_datetime()), timezone=TIME_ZONE)"))
    print("    Result: {}".format(tc.to_utc_datetime(tc.make_naive(tc.utc_datetime()), timezone=TIME_ZONE)))
    print()
    print(">> to_local_datetime(utc_dt, timezone=TIME_ZONE)")
    print("    Exec: {}".format("tc.to_local_datetime(datetime.datetime.utcnow(), timezone=TIME_ZONE)"))
    print("    Result: {}".format(tc.to_local_datetime(datetime.datetime.utcnow(), timezone=TIME_ZONE)))
    print("    Exec: {}".format("tc.to_local_datetime(tc.utc_datetime(), timezone=TIME_ZONE)"))
    print("    Result: {}".format(tc.to_local_datetime(tc.utc_datetime(), timezone=TIME_ZONE)))
    print()
    print(">> yesterday_utc_datetime()")
    print("    Exec: {}".format("tc.yesterday_utc_datetime()"))
    print("    Result: {}".format(tc.yesterday_utc_datetime()))
    print()
    print(">> tomorrow_utc_datetime()")
    print("    Exec: {}".format("tc.tomorrow_utc_datetime()"))
    print("    Result: {}".format(tc.tomorrow_utc_datetime()))
    print()
    print(">> yesterday_local_datetime()")
    print("    Exec: {}".format("tc.yesterday_local_datetime()"))
    print("    Result: {}".format(tc.yesterday_local_datetime()))
    print()
    print(">> tomorrow_local_datetime()")
    print("    Exec: {}".format("tc.tomorrow_local_datetime()"))
    print("    Result: {}".format(tc.tomorrow_local_datetime()))
    print()

    # STRING

    print(">> utc_string(utc_dt=None, format=TIME_FORMAT)")
    print("    Exec: {}".format("tc.utc_string(utc_dt=None, format=TIME_FORMAT)"))
    print("    Result: {}".format(tc.utc_string(utc_dt=None, format=TIME_FORMAT)))
    print()
    print(">> local_string(local_dt=None, format=TIME_FORMAT)")
    print("    Exec: {}".format("tc.local_string(local_dt=None, format=TIME_FORMAT)"))
    print("    Result: {}".format(tc.local_string(local_dt=None, format=TIME_FORMAT)))
    print()
    print(">> datetime_to_string(dt, format=TIME_FORMAT)")
    print("    Exec: {}".format("tc.datetime_to_string(datetime.datetime.now(), format=TIME_FORMAT)"))
    print("    Result: {}".format(tc.datetime_to_string(datetime.datetime.now(), format=TIME_FORMAT)))
    print()

    # TIMESTAMP

    print(">> utc_timestamp(utc_dt=None)")
    print("    Exec: {}".format("tc.utc_timestamp(utc_dt=None)"))
    print("    Result: {}".format(tc.utc_timestamp(utc_dt=None)))
    print()
    print(">> local_timestamp(local_dt=None)")
    print("    Exec: {}".format("tc.local_timestamp(local_dt=None)"))
    print("    Result: {}".format(tc.local_timestamp(local_dt=None)))
    print()
    print(">> datetime_to_timestamp(dt, format=TIME_FORMAT)")
    print("    Exec: {}".format("tc.datetime_to_timestamp(datetime.datetime.now())"))
    print("    Result: {}".format(tc.datetime_to_timestamp(datetime.datetime.now())))
    print()

    # STRING ==> DATETIME

    print(">> string_to_utc_datetime(string, format=TIME_FORMAT)")
    print("    Exec: {}".format("tc.string_to_utc_datetime('2015-10-04 12:12:12', format=TIME_FORMAT)"))
    print("    Result: {}".format(tc.string_to_utc_datetime('2015-10-04 12:12:12', format=TIME_FORMAT)))
    print()
    print(">> string_to_local_datetime(string, format=TIME_FORMAT)")
    print("    Exec: {}".format("tc.string_to_local_datetime('2015-10-04 12:12:12', format=TIME_FORMAT)"))
    print("    Result: {}".format(tc.string_to_local_datetime('2015-10-04 12:12:12', format=TIME_FORMAT)))
    print()
    print(">> utc_string_to_utc_datetime(utc_string, format=TIME_FORMAT)")
    print("    Exec: {}".format("tc.utc_string_to_utc_datetime('2015-10-04 12:12:12', format=TIME_FORMAT)"))
    print("    Result: {}".format(tc.utc_string_to_utc_datetime('2015-10-04 12:12:12', format=TIME_FORMAT)))
    print()

    # STRING ==> TIMESTAMP

    print(">> string_to_timestamp(string, format=TIME_FORMAT)")
    print("    Exec: {}".format("tc.string_to_timestamp('2015-10-04 12:12:12', format=TIME_FORMAT)"))
    print("    Result: {}".format(tc.string_to_timestamp('2015-10-04 12:12:12', format=TIME_FORMAT)))
    print()
    print(">> string_to_utc_timestamp(string, format=TIME_FORMAT)")
    print("    Exec: {}".format("tc.string_to_utc_timestamp('2015-10-04 12:12:12', format=TIME_FORMAT)"))
    print("    Result: {}".format(tc.string_to_utc_timestamp('2015-10-04 12:12:12', format=TIME_FORMAT)))
    print()
    print(">> string_to_local_timestamp(string, format=TIME_FORMAT)")
    print("    Exec: {}".format("tc.string_to_local_timestamp('2015-10-04 12:12:12', format=TIME_FORMAT)"))
    print("    Result: {}".format(tc.string_to_local_timestamp('2015-10-04 12:12:12', format=TIME_FORMAT)))
    print()

    # TIME_DELTA

    print(">> timestamp_delta(stamp1, stamp2)")
    print("    Exec: {}".format("tc.timestamp_delta(tc.utc_timestamp(), tc.utc_timestamp() + 10000)"))
    print("    Result: {}".format(tc.timestamp_delta(tc.utc_timestamp(), tc.utc_timestamp() + 10000)))
    print()
    print(">> datetime_delta(dt1, dt2)")
    print("    Exec: {}".format("tc.datetime_delta(tc.utc_datetime(), tc.tomorrow_utc_datetime())"))
    print("    Result: {}".format(tc.datetime_delta(tc.utc_datetime(), tc.tomorrow_utc_datetime())))
    print()
    print(">> string_delta(string1, string2, format=TIME_FORMAT, format1='', format2='')")
    print("    Exec: {}".format("tc.string_delta('2015-09-10 10:10:10', '2015-09-09 09:09:09')"))
    print("    Result: {}".format(tc.string_delta('2015-09-10 10:10:10', '2015-09-09 09:09:09')))
    print()

    # TIME_COUNT_DOWN

    print(">> timestamp_countdown(stamp)")
    print("    Exec: {}".format("tc.timestamp_countdown(tc.utc_timestamp() + 10000)"))
    print("    Result: {}".format(tc.timestamp_countdown(tc.utc_timestamp() + 10000)))
    print()
    print(">> datetime_countdown(dt)")
    print("    Exec: {}".format("tc.datetime_countdown(tc.tomorrow_utc_datetime())"))
    print("    Result: {}".format(tc.datetime_countdown(tc.tomorrow_utc_datetime())))
    print()
    print(">> string_countdown(string, format=TIME_FORMAT)")
    print("    Exec: {}".format("tc.string_countdown('2999-09-09 09:09:09')"))
    print("    Result: {}".format(tc.string_countdown('2999-09-09 09:09:09')))
    print()

    # AWARE vs NAIVE

    print(">> is_aware(value)")
    print("    Exec: {}".format("tc.is_aware(tc.utc_datetime())"))
    print("    Result: {}".format(tc.is_aware(tc.utc_datetime())))
    print()
    print(">> make_naive(value, timezone=TIME_ZONE)")
    print("    Exec: {}".format("tc.make_naive(tc.utc_datetime(), timezone=TIME_ZONE)"))
    print("    Result: {}".format(tc.make_naive(tc.utc_datetime(), timezone=TIME_ZONE)))
    print()
    print(">> is_naive(value)")
    print("    Exec: {}".format("tc.is_naive(datetime.datetime.now())"))
    print("    Result: {}".format(tc.is_naive(datetime.datetime.now())))
    print()
    print(">> make_aware(value, timezone=TIME_ZONE)")
    print("    Exec: {}".format("tc.make_aware(datetime.datetime.now(), timezone=TIME_ZONE)"))
    print("    Result: {}".format(tc.make_aware(datetime.datetime.now(), timezone=TIME_ZONE)))
    print()


if __name__ == '__main__':
    main()

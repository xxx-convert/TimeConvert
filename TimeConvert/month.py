"""Class file for a Month object.
Provides various utilities for generating, manipulating, and displaying
months.
import months
>>> month = months.Month(2015, 4)
>>> print(month.full_display)
'April 2015'
>>> print(month.month_abbr)
'Apr'
>>> print(month + 9)
'2016-01'
>>> print(month.start_date)
datetime.date(2015, 4, 1)
>>> print(month.n_days)
30
>>> print(month.dates[-1])
datetime.date(2015, 4, 30)
>>> print(month.nth(-1))
datetime.date(2015, 4, 30)
>>> print(month.to(2015, 5))
[Month(2015, 4), Month(2015, 5)]
>>> print(month.distance(month + 3))
3
>>> print(month.gregorian_month_number)
24172
>>> print(int(month))
201504
>>> print(float(month))
201504.0
"""

import calendar
import datetime
from collections import namedtuple
from functools import wraps


def __utctoday():
    """Return today's date in UTC time."""
    return datetime.datetime.utcnow().date()


def _get(other):
    """Coerce an arbitrary object into a Month type.
    This is designed to be used in functions accepting arbitrary type
    arguments in an *args situation, in which the value is expected to be
    comparable to a Month.
    Accepted types:
    1. Month
    2. Date / Datetime
    3. Two-value tuples (in *args or as a single argument).
    4. Single-value lists/tuples containing one of the above.
    >>> __get((2018, 1))
    Month(2018, 1)
    """
    # check for valid types, return if its easy
    if isinstance(other, Month):
        return other
    if isinstance(other, (datetime.date, datetime.datetime)):
        return Month.from_date(other)
    elif not isinstance(other, (list, tuple)):
        raise TypeError('Cannot coerce %s to Month.' % type(other))

    # at this point other must be a list or tuple.
    # if it only has one value then try to get the first value,
    # it could be a valid type stuffed in *args.
    #
    # otherwise create from a two-value tuple
    if len(other) == 1:
        return _get(other[0])
    elif len(other) == 2:
        return Month(*other)
    else:
        raise ValueError(
            'Cannot coerce list/tuple of length %d to Month.' % len(other)
        )


def _handle_other_decorator(func):
    """Decorate functions to handle "other" Month-like arguments.
    The arguments are assumed to be within *args, while only a single
    value (the Month) is actually desired for the function's execution.
    The __get function coerces the value to a month and passes it to the
    decorated function.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, _get(args), **kwargs)

    return wrapper


class Month(namedtuple('Month', ['year', 'month'])):
    """Represent a specific month of a year.
    Provides various utilities for generating, manipulating, and displaying
    months.
    """

    def __init__(self, year, month):
        """Validate params."""
        if year == 0:
            raise ValueError('Year 0 is not valid in the Gregorian calendar.')
        if month < 1 or month > 12:
            raise ValueError('Month number must be 1-12.')

    def __repr__(self):
        """Return repr."""
        return (
            "%s(%d, %d)" % (self.__class__.__name__, self.year, self.month)
        )

    def __str__(self):
        """Return month in canonical YYYY-MM string format."""
        return self.start_date.strftime("%Y-%m")

    def __int__(self):
        """Return month in canonical YYYYMM integer format."""
        return int(self.start_date.strftime("%Y%m"))

    def __float__(self):
        """Return month in canonical YYYYMM format as a float."""
        return float(int(self))

    @property
    def month_name(self):
        """Return the calendar name of the month.
        >>> Month(2015, 4).month_name
        'April'
        """
        return calendar.month_name[self.month]

    @property
    def month_abbr(self):
        """Return the abbreviated calendar name of the month.
        >>> Month(2015, 4).month_abbr
        'Apr'
        """
        return calendar.month_abbr[self.month]

    @property
    def full_display(self):
        """Return the calendar name of the month along with the year.
        >>> Month(2015, 4).full_display
        'April 2015'
        """
        return "%s %d" % (self.month_name, self.year)

    @property
    def abbr_display(self):
        """Return the abbreviated calendar name of the month and the year.
        >>> Month(2015, 4).full_display
        'Apr 2015'
        """
        return "%s %d" % (self.month_abbr, self.year)

    @property
    def n_days(self):
        """Return the number of days in the month.
        >>> Month(2018, 1).n_days
        31
        """
        return calendar.monthrange(self.year, self.month)[1]

    @property
    def gregorian_month_number(self):
        """Return the number of months since the start of Gregorian year 1.
        Year 0 and month 0 are invalid. So the first month of year 1 is 1, and
        the first month of year -1 is -1.
        >>> Month(1, 1).gregorian_month_number
        1
        >>> Month(2, 2).gregorian_month_number
        14
        >>> Month(-1, 2).gregorian_month_number
        -2
        """
        if self.year > 0:
            return (self.year - 1) * 12 + self.month
        else:
            return (self.year + 1) * 12 - self.month

    @property
    def dates(self):
        """Return a tuple of all days in the month.
        >>> Month(2018, 1).dates[:2]
        (datetime.date(2018, 1, 1), datetime.date(2018, 1, 2))
        """
        return tuple(map(self.nth, range(1, self.n_days + 1)))

    @classmethod
    def from_date(cls, date):
        """Return a Month instance from given a date or datetime object.
        Parameters
        ----------
        date : date or datetime
            A date/datetime object as implemented via the standard lib module.
        Returns
        -------
        month : Month
            The month object for that date.
        """
        try:
            date = date.date()
        except AttributeError:
            pass
        return cls(date.year, date.month)

    @classmethod
    def from_today(cls):
        """Return a Month instance from today's date (local time)."""
        return cls.from_date(datetime.date.today())

    @classmethod
    def from_utc_today(cls):
        """Return a Month instance from today's date (UTC time)."""
        return cls.from_date(__utctoday())

    def __add__(self, other):
        """Offset a number of months into the future.
        >>> Month(2015, 4) + 9
        Month(2016, 1)
        Parameters
        ----------
        other : int
            Integer number of months to add.
        Returns
        -------
        month : Month
            The month object offset N months.
        """
        if not isinstance(other, int):
            raise TypeError("Only ints can be added to months")

        year_change, month = divmod(self.month + other - 1, 12)
        return type(self)(self.year + year_change, month + 1)

    def __sub__(self, other):
        """Offset a number of months into the past.
        >>> Month(2015, 4) - 9
        Month(2014, 7)
        Parameters
        ----------
        other : int
            Integer number of months to subtract.
        Returns
        -------
        month : Month
            The month object offset -N months.
        """
        # if not isinstance(other, int):
        #     raise TypeError("Only ints can be subtracted from months")
        #
        # return self + (-other)
        if isinstance(other, int):
            return self + (-other)

        return self.gregorian_month_number - other.gregorian_month_number

    @property
    def start_date(self):
        """Return a datetime.date object for the first day of the month."""
        return datetime.date(self.year, self.month, 1)

    @property
    def end_date(self):
        """Return a datetime.date object for the last day of the month."""
        return (self + 1).start_date - datetime.timedelta(1)

    @property
    def range(self):
        """Return a tuple of the first and last days of the month."""
        return (self.start_date, self.end_date)

    def nth(self, day):
        """Get date object for nth day of month.
        Accepts nonzero integer values between +- ``month.n_days``.
        >>> Month(2018, 1).nth(1) == Month(2018, 1).start_date
        True
        >>> Month(2018, 1).nth(8)
        datetime.date(2018, 1, 8)
        >>> Month(2018, 1).nth(-2)
        datetime.date(2018, 1, 30)
        Parameters
        ----------
        day : int
            Day of the month.
        Returns
        -------
        date : datetime.date
            Date object for the day of the month.
        """

        # validate param
        if day == 0:
            raise ValueError('Day of month must be nonzero!')
        if abs(day) > self.n_days:
            raise ValueError(
                'Day of month must be within +- %s for %s!' %
                (self.n_days, self.full_display)
            )

        if day < 0:
            day = self.n_days + 1 + day
        return datetime.date(self.year, self.month, day)

    @_handle_other_decorator
    def to(self, other):
        """Generate a list of all months between two months, inclusively.
        Accepts two-element lists/tuples, date-like objects, or Month objects.
        If months are provided out of order (like ``june_18.to.march_18``) then
        the list will also be in reverse order.
        >>> Month(2018, 1).to(Month(2018, 2))
        [Month(2018, 1), Month(2018, 2)]
        >>> Month(2018, 3).to(2018, 1)
        [Month(2018, 3), Month(2018, 2), Month(2018, 1)]
        Parameters
        ----------
        other : Month, date, datetime, tuple
            A Month-like object.
        Returns
        -------
        months : list
            List of months spanning the two objects, inclusively.
        """
        def walk(first, second):
            """TODO: Something more efficient than iterative walking."""
            assert first <= second
            months = [first]
            while months[-1] < second:
                months.append(months[-1] + 1)
            return months

        if self >= other:
            return walk(other, self)[::-1]
        else:
            return walk(self, other)

    @_handle_other_decorator
    def distance(self, other):
        """Return the number of months distance between months.
        This will always be a positive number. Accepts two-element lists/tuples
        or Month objects.
        >>> Month(2018, 1).distance(Month(2018, 12))
        11
        >>> Month(2018, 5).distance(2018, 1)
        4
        Parameters
        ----------
        other : Month, date, datetime, tuple
            A Month-like object.
        Returns
        -------
        n_months : int
            Integer number of months distance.
        """
        return abs(self.gregorian_month_number - other.gregorian_month_number)

import datetime
import math
from collections import namedtuple


def get_quarter_start_date(year, quarter):
    return {
        1: datetime.date(year, 1, 1),
        2: datetime.date(year, 4, 1),
        3: datetime.date(year, 7, 1),
        4: datetime.date(year, 10, 1),
    }.get(quarter)


def get_quarter_end_date(year, quarter):
    return {
        1: datetime.date(year, 3, 31),
        2: datetime.date(year, 6, 30),
        3: datetime.date(year, 9, 30),
        4: datetime.date(year, 12, 31),
    }.get(quarter)


class Quarter(namedtuple('Quarter', ('year', 'quarter'))):
    __slots__ = ()

    def __new__(cls, year, quarter):
        if quarter < 1 or quarter > 4:
            return cls(year, 1) + (quarter - 1)
        if year < 1 or year > 9999:
            raise ValueError('year is out of range')
        return super(Quarter, cls).__new__(cls, year, quarter)

    def __str__(self):
        return '%04dQ%01d' % self

    isoformat = __str__  # compatibility with datetime.date

    def __repr__(self):
        return __name__ + '.' + self.__class__.__name__ + '(%d, %d)' % self

    def __add__(self, other):
        if not isinstance(other, int):
            raise TypeError('Only ints can be added to quarter')

        year_change, quarter = divmod(self.quarter + other - 1, 4)
        return type(self)(self.year + year_change, quarter + 1)

    def __sub__(self, other):
        if isinstance(other, int):
            return self + (-other)

        return self.gregorian_quarter_number - other.gregorian_quarter_number

    @property
    def gregorian_quarter_number(self):
        if self.year > 0:
            return (self.year - 1) * 4 + self.quarter
        else:
            return (self.year + 1) * 4 - self.quarter

    @classmethod
    def from_date(cls, date):
        return cls(*(date.year, int(math.ceil(date.month / 3))))

    withdate = fromdate = from_date

    @property
    def start_date(self):
        return get_quarter_start_date(self.year, self.quarter)

    @property
    def end_date(self):
        return get_quarter_end_date(self.year, self.quarter)

    startdate = start_date
    enddate = end_date

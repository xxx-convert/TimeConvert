import sys
from collections import namedtuple
from datetime import timedelta


if sys.version >= '3':
    # compatiblity tweaks
    basestring = str
    long = int


class Week(namedtuple('Week', ('year', 'week', 'mode'))):
    __slots__ = ()

    def __new__(cls, year, week, mode=3):
        """Initialize a Week tuple with the given year and week number."""
        if year < 1 or year > 9999:
            raise ValueError("year is out of range")
        return super(Week, cls).__new__(cls, year, week, mode)

    @classmethod
    def fromstring(cls, isostring, mode=3):
        """Return a week initialized from an ISO formatted string like "2011W08" or "2011-W08"."""
        if isinstance(isostring, basestring) and len(isostring) == 7 and isostring[4] == 'W':
            return cls(int(isostring[0:4]), int(isostring[5:7]), mode=mode)
        if isinstance(isostring, basestring) and len(isostring) == 8 and isostring[4:6] == '-W':
            return cls(int(isostring[0:4]), int(isostring[6:8]), mode=mode)
        raise ValueError("Week.tostring argument must be on the form <yyyy>W<ww>; got %r" % (isostring,))

    def __str__(self):
        """Return a ISO formatted week string like "2011W08". """
        return '%04dW%02d' % (self.year, self.week)

    isoformat = __str__  # compatibility with datetime.date

    def __repr__(self):
        """Return a string like "isoweek.Week(2011, 35)"."""
        return __name__ + '.' + self.__class__.__name__ + '(%d, %d)' % (self.year, self.week)


Week.min = Week(1, 1)
Week.max = Week(9999, 52)
Week.resolution = timedelta(weeks=1)

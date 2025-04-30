import datetime
from itertools import ifilter, imap, islice, takewhile
import requests


BANK_HOLIDAYS_URL = 'https://www.gov.uk/bank-holidays/england-and-wales.json'

SLOT_INTERVAL_MINS = 30


def current_datetime():
    # this function is to make unit testing simpler
    return datetime.datetime.now()


def in_the_past(time):
    return current_datetime() > time


def before_9am(time):
    return time.time() < datetime.time(9, 0)


def after_8pm(time):
    return time.time() >= datetime.time(20, 0)


def on_sunday(time):
    return time.weekday() == 6


def parse_date(text):
    return datetime.datetime.strptime(text, '%Y-%m-%d')


def get_date(bank_holiday):
    return parse_date(bank_holiday['date'])


class BankHolidays(object):

    def __init__(self):
        self._cache = None
        self.init_cache()

    def init_cache(self):
        from django.core.cache import cache
        self._cache = cache

    @property
    def url(self):
        return BANK_HOLIDAYS_URL

    @property
    def dates(self):
        dates = self._cached_dates

        if not dates:
            dates = self._parse_dates(self._load_dates())
            self._cached_dates = dates

        return dates

    @property
    def _cached_dates(self):
        if self._cache:
            return self._cache.get('bank_holidays')

    @_cached_dates.setter
    def _cached_dates(self, dates):
        if self._cache:
            one_year = 365 * 24 * 60 * 60
            self._cache.set('bank_holidays', dates, one_year)

    def _load_dates(self):
        return requests.get(self.url).json()['events']

    def _parse_dates(self, events):
        return map(get_date, events)

    def __contains__(self, day):
        return day in self.dates


def bank_holidays():
    return BankHolidays()


def on_bank_holiday(time):
    day = datetime.datetime.combine(time.date(), datetime.time())
    return day in bank_holidays()


def on_saturday(time):
    return time.weekday() == 5


def on_weekday(time):
    return time.weekday() < 5


def after_1230(time):
    return time.time() >= datetime.time(12, 30)


def is_today(time):
    return time.date() == current_datetime().date()


def too_late(time):
    start = current_datetime() + datetime.timedelta(hours=2)
    return time.time() < start.time()


def available(dt, ignore_time=False):
    if not (in_the_past(dt) or on_sunday(dt) or on_bank_holiday(dt)):
        return ignore_time or not (
            (before_9am(dt) or after_8pm(dt)) or
            (on_saturday(dt) and after_1230(dt)))
    return False


def can_schedule_callback(dt):
    if is_today(dt) and too_late(dt):
        return False
    return available(dt)


def every_interval(time, days=0, hours=0, minutes=0):
    interval = datetime.timedelta(days=days, hours=hours, minutes=minutes)
    while True:
        yield time
        time += interval


def available_days(num):
    days = every_interval(current_datetime(), days=1)
    available_day = lambda day: available(day, ignore_time=True)
    return list(islice(ifilter(available_day, days), num))


def time_slots(day=None):
    if not day:
        day = datetime.date(9999, 1, 1)  # a weekday in the future
    start = datetime.datetime.combine(day, datetime.time(9))
    today = current_datetime()
    same_day = lambda x: x.date() == day
    slots = takewhile(
        same_day, every_interval(start, minutes=SLOT_INTERVAL_MINS))
    is_available = lambda slot: can_schedule_callback(slot)
    return list(ifilter(is_available, slots))


def today_slots(*args):
    return time_slots(current_datetime().date())


def tomorrow_slots(*args):
    tomorrow = current_datetime() + datetime.timedelta(days=1)
    return time_slots(tomorrow.date())


class Hours(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, dt):
        return self.start <= dt.time() < self.end


class OpeningHours(object):

    def __init__(
            self,
            weekday=None,
            saturday=None,
            sunday=None,
            bank_holiday=None,
            **kwargs):

        def date_matcher(key):
            date = datetime.datetime.strptime(key, '%Y-%m-%d').date()
            return lambda dt: dt.date() == date

        hours = lambda args: args and Hours(*args)

        self.day_hours = [
            (date_matcher(key), hours(val)) for key, val in kwargs.iteritems()
        ]

        self.day_hours.append((on_bank_holiday, hours(bank_holiday)))
        self.day_hours.append((on_sunday, hours(sunday)))
        self.day_hours.append((on_saturday, hours(saturday)))
        self.day_hours.append((on_weekday, hours(weekday)))

    def __contains__(self, dt):
        return self.available(dt)

    def available(self, dt, ignore_time=False):
        for (on_day, hours) in self.day_hours:
            if on_day(dt):
                if hours is None:
                    return False
                if not ignore_time and dt not in hours:
                    return False

        return True

    def can_schedule_callback(self, dt, ignore_time=False):
        if in_the_past(dt):
            return False
        if is_today(dt) and too_late(dt):
            return False
        return self.available(dt, ignore_time=ignore_time)

    def time_slots(self, day=None):
        if not day:
            day = datetime.date(9999, 1, 1)  # a weekday in the future
        start = datetime.datetime.combine(day, datetime.time(0))
        today = current_datetime()
        same_day = lambda dt: dt.date() == day
        available = lambda dt: self.can_schedule_callback(dt)
        return list(ifilter(available, takewhile(same_day, every_interval(
            start, minutes=SLOT_INTERVAL_MINS))))

    def today_slots(self):
        return self.time_slots(current_datetime().date())

    def tomorrow_slots(self):
        tomorrow = current_datetime() + datetime.timedelta(days=1)
        return self.time_slots(tomorrow.date())

    def available_days(self, num_days=6):
        start = current_datetime() + datetime.timedelta(days=1)
        days = every_interval(start, days=1)
        available_day = lambda day: self.can_schedule_callback(day, ignore_time=True)
        return list(islice(ifilter(available_day, days), num_days))

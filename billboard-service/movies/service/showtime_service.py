from ..models import Showtime, Theater
from django.utils import timezone
from datetime import datetime

class ShowTimeService:
    OPENING_HOUR = 11
    CLOSE_HOUR = 23
    MIN_PRICE = 5 
    MAX_PRICE = 250
    MOVIE_DURATION_LIMIT = 5 # Hours

    def validate_persistence(self, data, is_update=False):
        price = data.get('price')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        theater = data.get('theater')

        self.__validate_price(price)
        self.__validate_schedule(theater, start_time, end_time, is_update)        

        return True

    def __validate_price(self, price):
        if price < self.MIN_PRICE or price > self.MAX_PRICE:
            raise ValueError("price not valid. (Valid range: 5 to 250)")

    def __validate_schedule(self, theater, start_time, end_time, is_update):
        if start_time.hour < self.OPENING_HOUR or start_time.hour >= self.CLOSE_HOUR:
            raise ValueError("Schedule conflict. A Showtime doesn't follow the cinema service schedule (Schedule: 11:00-23:00)")

        if start_time > end_time:
            raise ValueError("Schedule error. Showtime start date can't be after the end date")

        duration = (end_time - start_time).total_seconds() / 3600 
        if duration > self.MOVIE_DURATION_LIMIT:
            raise ValueError(f"Schedule error. Showtime duration can't be longer than {self.MOVIE_DURATION_LIMIT} hours")

        if not is_update:
            existing_showtime = Showtime.objects.filter(
                start_time__lt=end_time, 
                end_time__gt=start_time,
                theater=theater
            ).first()

            if existing_showtime:
                raise ValueError("Schedule conflict. A Showtime already exists in that theater and schedule")

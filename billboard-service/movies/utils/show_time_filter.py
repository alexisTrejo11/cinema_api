from datetime import datetime

class ShowtimeSearchFilter:
    def __init__(self):
        self.filters = {}

    def by_cinema(self, cinema_id):
        if cinema_id:
            self.filters['cinema_id'] = cinema_id
        return self

    def by_movie(self, movie_id):
        if movie_id:
            self.filters['movie_id'] = movie_id
        return self
    
    def by_theater(self, theater_id):
        if theater_id:
            self.filters['theater_id'] = theater_id
        return self

    def by_start_time(self, start_time):
        if start_time:
            try:
                start_time = datetime.fromisoformat(start_time)
                self.filters['start_time'] = start_time
            except ValueError:
                raise ValueError("Invalid start_time format.")
        return self

    def by_end_time(self, end_time):
        if end_time:
            try:
                end_time = datetime.fromisoformat(end_time)
                self.filters['end_time'] = end_time
            except ValueError:
                raise ValueError("Invalid end_time format.")
        return self

    def build(self):
        return self.filters

class MovieFilter:
    def __init__(self):
        self.title = None
        self.duration = None
        self.genre = None
        self.rating = None
        self.end_date = None
        self.is_active = None

    def add_title(self, title):
        self.title = title
        return self

    def add_duration(self, duration):
        self.duration = duration
        return self

    def add_genre(self, genre):
        self.genre = genre
        return self

    def add_rating(self, rating):
        self.rating = rating
        return self

    def add_end_date(self, end_date):
        self.end_date = end_date
        return self

    def add_is_active(self, is_active):
        self.is_active = is_active
        return self

    def build(self):
        return self

class Object:
    def __init__(self,
                 object_type: str,
                 launch_year: int,
                 decay_year: int,
                 apogee: float,
                 perigee: float,
                 ):
        self.object_type = object_type
        self.launch_year = launch_year
        self.decay_year = decay_year
        self.apogee = apogee
        self.perigee = perigee

    def is_in_range(self, low, high) -> bool:
        if low < self.apogee or self.perigee > high:
            return False
        return True

    def is_alive_in_year(self, year) -> bool:
        if self.launch_year <= year <= self.decay_year:
            return True
        return False

    def __str__(self):
        return (f"Object type {self.object_type}, launch year {self.launch_year}, decay year {self.decay_year}, apogee "
                + f"{self.apogee}, perigee {self.perigee}")

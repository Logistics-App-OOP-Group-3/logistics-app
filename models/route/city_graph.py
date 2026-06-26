from enums.city import City as c

class CityGraph:

    SPEED_KMH = 87
    
    DISTANCES = {
        c.SYD: {c.MEL: 877,  c.ADL: 1376, c.ASP: 2762, c.BRI: 909,  c.DAR: 3935, c.PER: 4016},
        c.MEL: {c.SYD: 877,  c.ADL: 725,  c.ASP: 2255, c.BRI: 1765, c.DAR: 3752, c.PER: 3509},
        c.ADL: {c.SYD: 1376, c.MEL: 725,  c.ASP: 1530, c.BRI: 1927, c.DAR: 3027, c.PER: 2785},
        c.ASP: {c.SYD: 2762, c.MEL: 2255, c.ADL: 1530, c.BRI: 2993, c.DAR: 1497, c.PER: 2481},
        c.BRI: {c.SYD: 909,  c.MEL: 1765, c.ADL: 1927, c.ASP: 2993, c.DAR: 3426, c.PER: 4311},
        c.DAR: {c.SYD: 3935, c.MEL: 3752, c.ADL: 3027, c.ASP: 1497, c.BRI: 3426, c.PER: 4025},
        c.PER: {c.SYD: 4016, c.MEL: 3509, c.ADL: 2785, c.ASP: 2481, c.BRI: 4311, c.DAR: 4025},
    }
    
    # DISTANCES = {
    #     "SYD": {"MEL": 877,  "ADL": 1376, "ASP": 2762, "BRI": 909,  "DAR": 3935, "PER": 4016},
    #     "MEL": {"SYD": 877,  "ADL": 725,  "ASP": 2255, "BRI": 1765, "DAR": 3752, "PER": 3509},
    #     "ADL": {"SYD": 1376, "MEL": 725,  "ASP": 1530, "BRI": 1927, "DAR": 3027, "PER": 2785},
    #     "ASP": {"SYD": 2762, "MEL": 2255, "ADL": 1530, "BRI": 2993, "DAR": 1497, "PER": 2481},
    #     "BRI": {"SYD": 909,  "MEL": 1765, "ADL": 1927, "ASP": 2993, "DAR": 3426, "PER": 4311},
    #     "DAR": {"SYD": 3935, "MEL": 3752, "ADL": 3027, "ASP": 1497, "BRI": 3426, "PER": 4025},
    #     "PER": {"SYD": 4016, "MEL": 3509, "ADL": 2785, "ASP": 2481, "BRI": 4311, "DAR": 4025},
    # }

    @classmethod
    def distance(cls, a: c, b: c) -> int:
        return cls.DISTANCES[a][b]

    @classmethod
    def travel_time_hours(cls, distance: float) -> float:
        return distance / cls.SPEED_KMH
    
        
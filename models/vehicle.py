
class Vehicle:
    
    vehicles_csv_line = [
        "1001-1010,Scania,42_000,8_000,",
        "1011-1025,Man,37_000,10_000",
        "1026-1040,Actros,26_000,13_000"
    ]
    
    def __init__(self, id:int, name: str, capacity: int, max_range: int):
        self._id = id
        self._name = name
        self._capacity = capacity
        self._max_range = max_range # kilometers
        
    @property             # id
    def id(self):
        return self._id
    @property             # name
    def name(self):
        return self._name
    @property             # capacity
    def capacity(self):
        return self._capacity  
    @property             # max_range
    def max_range(self):
        return self._max_range
        
    @classmethod
    def from_csv(cls, input_line: str = None) -> Vehicle:
        tokens = input_line.split(',')
        id = int(tokens[0])
        name = tokens[1]
        capacity = int(tokens[2])
        max_range = int(tokens[3])
        
        return cls(id, name, capacity, max_range)
    
    def __str__(self):
        return f"{self._id}.{self.name} MaxCapacity: {self.capacity} MaxKMRange:{self.max_range}"
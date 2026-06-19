
class Vehicle:
    def __init__(self, name: str, capacity: int, max_range: int):
        self._name = name
        self._capacity = capacity
        self._max_range = max_range
        
    @property             #name
    def name(self):
        return self._name
    @property             #capacity
    def capacity(self):
        return self._capacity  
    @property             #max_range
    def max_range(self):
        return self._max_range
        
    @classmethod
    def from_csv(cls, input_line: str) -> Vehicle:
        tokens = input_line.split(',')
        name = tokens[0]
        capacity = int(tokens[1])
        max_range = int(tokens[2])
        
        return cls(name, capacity, max_range)
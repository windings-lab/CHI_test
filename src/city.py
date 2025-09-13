from dataclasses import dataclass

@dataclass
class City:
    name: str
    country: str
    lat: float
    lon: float

    @classmethod
    def from_dict(cls, data: dict):
        filtered_data = {k: v for k, v in data.items() if k in cls.__annotations__}

        return cls(**filtered_data)
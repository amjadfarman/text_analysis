configurations = {
    "scrape": False,
    "main_address": "https://www.main_path/speeches",
    "speech_addresses": (
        "speech_sub_path",
    ),
    "interval": 2,
}

class Config:
    def __init__(self) -> None:
        self.conf = configurations

    def get_property(self, property_name: str):
        value = None
        if property_name in self.conf:
            value = self.conf[property_name]
        return value
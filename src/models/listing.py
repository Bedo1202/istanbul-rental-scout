
from dataclasses import dataclass


@dataclass
class Listing:
    source: str
    source_listing_id: str
    title: str
    price: int
    district: str
    room_type: str
    furnished: bool | None
    listing_url: str

    neighborhood: str | None = None
    building_age: int | None = None
    metro_walking_minutes: int | None = None

    def get_unique_key(self):
        return f"{self.source}:{self.source_listing_id}"

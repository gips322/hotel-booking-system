"""Модель гостиницы"""

from typing import Dict, Any, List
from .base_entity import BaseEntity
from .room import Room


class Hotel(BaseEntity):
    def __init__(self, hotel_id: str, name: str, address: str, rating: float = 3.0, phone: str = ""):
        super().__init__(hotel_id)
        self._name = name
        self._address = address
        self._rating = rating
        self._phone = phone
        self._rooms: List[Room] = []
        self._description = ""
    
    def get_name(self) -> str:
        return self._name
    
    def set_name(self, name: str):
        self._name = name
        self.update_timestamp()
    
    def get_address(self) -> str:
        return self._address
    
    def get_rating(self) -> float:
        return self._rating
    
    def get_phone(self) -> str:
        return self._phone
    
    def set_description(self, desc: str):
        self._description = desc
        self.update_timestamp()
    
    def add_room(self, room: Room):
        if any(r.get_room_number() == room.get_room_number() for r in self._rooms):
            raise ValueError(f"Номер {room.get_room_number()} уже существует в гостинице {self._name}")
        self._rooms.append(room)
        self.update_timestamp()
    
    def remove_room(self, room_number: str):
        self._rooms = [r for r in self._rooms if r.get_room_number() != room_number]
        self.update_timestamp()
    
    def get_rooms(self) -> List[Room]:
        return self._rooms
    
    def get_total_rooms(self) -> int:
        return len(self._rooms)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "hotel_id": self._id,
            "name": self._name,
            "address": self._address,
            "rating": self._rating,
            "phone": self._phone,
            "description": self._description,
            "rooms": [room.to_dict() for room in self._rooms],
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Hotel':
        hotel = Hotel(data["hotel_id"], data["name"], data["address"],
                      data.get("rating", 3.0), data.get("phone", ""))
        hotel._description = data.get("description", "")
        hotel._created_at = data.get("created_at", "")
        hotel._updated_at = data.get("updated_at", "")
        for room_data in data.get("rooms", []):
            hotel.add_room(Room.from_dict(room_data))
        return hotel
    
    def __str__(self) -> str:
        return f"{self._name} ★{self._rating} ({self._address}), ID: {self._id}, Номеров: {len(self._rooms)}"
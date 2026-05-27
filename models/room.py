"""Модель номера"""

from typing import Dict, Any, List
from .base_entity import BaseEntity


class Room(BaseEntity):
    def __init__(self, room_number: str, price_per_night: float, capacity: int,
                 amenities: List[str] = None, floor: int = 1):
        super().__init__(room_number)
        self._price_per_night = price_per_night
        self._capacity = capacity
        self._amenities = amenities or []
        self._floor = floor
        self._is_maintenance = False
    
    def get_room_number(self) -> str:
        return self._id
    
    def get_price(self) -> float:
        return self._price_per_night
    
    def set_price(self, price: float):
        self._price_per_night = price
        self.update_timestamp()
    
    def get_capacity(self) -> int:
        return self._capacity
    
    def get_amenities(self) -> List[str]:
        return self._amenities
    
    def set_maintenance(self, status: bool):
        self._is_maintenance = status
        self.update_timestamp()
    
    def is_available_for_booking(self) -> bool:
        return not self._is_maintenance
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "room_number": self._id,
            "price_per_night": self._price_per_night,
            "capacity": self._capacity,
            "amenities": self._amenities,
            "floor": self._floor,
            "is_maintenance": self._is_maintenance,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Room':
        room = Room(data["room_number"], data["price_per_night"],
                    data["capacity"], data.get("amenities", []), data.get("floor", 1))
        room._is_maintenance = data.get("is_maintenance", False)
        room._created_at = data.get("created_at", "")
        room._updated_at = data.get("updated_at", "")
        return room
    
    def __str__(self) -> str:
        maint = " [РЕМОНТ]" if self._is_maintenance else ""
        return f"Номер {self._id}{maint} - {self._price_per_night}₽/ночь, {self._capacity} чел., Этаж {self._floor}"
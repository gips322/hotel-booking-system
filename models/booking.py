"""Модель бронирования"""

from typing import Dict, Any
from datetime import datetime
from .base_entity import BaseEntity


class Booking(BaseEntity):
    def __init__(self, booking_id: str, hotel_id: str, room_number: str, guest_id: str,
                 check_in: str, check_out: str, total_price: float = 0, status: str = "active"):
        super().__init__(booking_id)
        self._hotel_id = hotel_id
        self._room_number = room_number
        self._guest_id = guest_id
        self._check_in = check_in
        self._check_out = check_out
        self._total_price = total_price
        self._status = status
        self._special_requests = ""
    
    def get_hotel_id(self) -> str:
        return self._hotel_id
    
    def get_room_number(self) -> str:
        return self._room_number
    
    def get_guest_id(self) -> str:
        return self._guest_id
    
    def get_check_in(self) -> str:
        return self._check_in
    
    def get_check_out(self) -> str:
        return self._check_out
    
    def get_status(self) -> str:
        return self._status
    
    def set_status(self, status: str):
        self._status = status
        self.update_timestamp()
    
    def get_total_price(self) -> float:
        return self._total_price
    
    def set_total_price(self, price: float):
        self._total_price = price
        self.update_timestamp()
    
    def get_nights_count(self) -> int:
        start = datetime.strptime(self._check_in, "%Y-%m-%d")
        end = datetime.strptime(self._check_out, "%Y-%m-%d")
        return (end - start).days
    
    def overlaps(self, other: 'Booking') -> bool:
        start1 = datetime.strptime(self._check_in, "%Y-%m-%d")
        end1 = datetime.strptime(self._check_out, "%Y-%m-%d")
        start2 = datetime.strptime(other._check_in, "%Y-%m-%d")
        end2 = datetime.strptime(other._check_out, "%Y-%m-%d")
        return max(start1, start2) < min(end1, end2)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "booking_id": self._id,
            "hotel_id": self._hotel_id,
            "room_number": self._room_number,
            "guest_id": self._guest_id,
            "check_in": self._check_in,
            "check_out": self._check_out,
            "total_price": self._total_price,
            "status": self._status,
            "special_requests": self._special_requests,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Booking':
        booking = Booking(data["booking_id"], data["hotel_id"], data["room_number"],
                          data["guest_id"], data["check_in"], data["check_out"],
                          data.get("total_price", 0), data.get("status", "active"))
        booking._special_requests = data.get("special_requests", "")
        booking._created_at = data.get("created_at", datetime.now().isoformat())
        booking._updated_at = data.get("updated_at", datetime.now().isoformat())
        return booking
    
    def __str__(self) -> str:
        status_ru = "Активно" if self._status == "active" else "Отменено"
        return f"Бронь {self._id}: Номер {self._room_number} (отель {self._hotel_id}) для гостя {self._guest_id} | {self._check_in} → {self._check_out} | {self._total_price}₽ | {status_ru}"
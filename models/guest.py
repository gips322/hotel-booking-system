"""Модель гостя"""

from typing import Dict, Any
from datetime import datetime
from .base_entity import BaseEntity


class Guest(BaseEntity):
    def __init__(self, guest_id: str, name: str, contact: str, email: str = ""):
        super().__init__(guest_id)
        self._name = name
        self._contact = contact
        self._email = email
        self._loyalty_points = 0
    
    def get_name(self) -> str:
        return self._name
    
    def set_name(self, name: str):
        self._name = name
        self.update_timestamp()
    
    def get_contact(self) -> str:
        return self._contact
    
    def set_contact(self, contact: str):
        self._contact = contact
        self.update_timestamp()
    
    def get_email(self) -> str:
        return self._email
    
    def add_loyalty_points(self, points: int):
        self._loyalty_points += points
        self.update_timestamp()
    
    def get_loyalty_points(self) -> int:
        return self._loyalty_points
    
    def get_info(self) -> str:
        return f"[Гость {self._id}] {self._name}, Тел.: {self._contact}, Email: {self._email}, Баллы: {self._loyalty_points}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "guest_id": self._id,
            "name": self._name,
            "contact": self._contact,
            "email": self._email,
            "loyalty_points": self._loyalty_points,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Guest':
        guest = Guest(data["guest_id"], data["name"], data["contact"], data.get("email", ""))
        guest._loyalty_points = data.get("loyalty_points", 0)
        guest._created_at = data.get("created_at", datetime.now().isoformat())
        guest._updated_at = data.get("updated_at", datetime.now().isoformat())
        return guest
    
    def __str__(self) -> str:
        return self.get_info()
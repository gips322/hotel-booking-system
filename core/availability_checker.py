"""Проверка доступности номеров"""

from typing import List
from models.room import Room
from models.booking import Booking


class AvailabilityChecker:
    """Класс для проверки доступности номеров"""
    
    @staticmethod
    def is_room_free(room: Room, bookings: List[Booking], date: str) -> bool:
        """Проверяет, свободен ли номер на конкретную дату"""
        if not room.is_available_for_booking():
            return False
        
        for booking in bookings:
            if booking.get_status() != "active":
                continue
            if booking.get_room_number() != room.get_room_number():
                continue
            if booking.get_check_in() <= date < booking.get_check_out():
                return False
        return True
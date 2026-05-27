"""Менеджер бронирований (бизнес-логика)"""

from typing import List, Tuple, Optional
from datetime import datetime
from models.booking import Booking
from models.hotel import Hotel
from models.guest import Guest
from models.room import Room
from core.validators import validate_date_range
from core.availability_checker import AvailabilityChecker


class BookingManager:
    """Управление бронированиями"""
    
    def __init__(self, hotels: List[Hotel], guests: List[Guest], bookings: List[Booking]):
        self._hotels = hotels
        self._guests = guests
        self._bookings = bookings
    
    def _find_hotel(self, hotel_id: str) -> Optional[Hotel]:
        for hotel in self._hotels:
            if hotel.get_id() == hotel_id:
                return hotel
        return None
    
    def _find_room(self, hotel: Hotel, room_number: str) -> Optional[Room]:
        for room in hotel.get_rooms():
            if room.get_room_number() == room_number:
                return room
        return None
    
    def _find_guest(self, guest_id: str) -> Optional[Guest]:
        for guest in self._guests:
            if guest.get_id() == guest_id:
                return guest
        return None
    
    def _calculate_price(self, room: Room, check_in: str, check_out: str) -> float:
        start = datetime.strptime(check_in, "%Y-%m-%d")
        end = datetime.strptime(check_out, "%Y-%m-%d")
        nights = (end - start).days
        if nights <= 0:
            return 0
        base_price = room.get_price() * nights
        if nights >= 7:
            base_price *= 0.9
        return round(base_price, 2)
    
    def _check_overlap(self, new_booking: Booking) -> bool:
        for existing in self._bookings:
            if existing.get_status() != "active":
                continue
            if existing.get_hotel_id() != new_booking.get_hotel_id():
                continue
            if existing.get_room_number() != new_booking.get_room_number():
                continue
            if new_booking.overlaps(existing):
                return True
        return False
    
    def create_booking(self, hotel_id: str, room_number: str, guest_id: str,
                      check_in: str, check_out: str) -> Tuple[bool, str, Optional[Booking]]:
        hotel = self._find_hotel(hotel_id)
        if not hotel:
            return False, "Гостиница не найдена", None
        
        room = self._find_room(hotel, room_number)
        if not room:
            return False, "Номер не найден в этой гостинице", None
        
        if not room.is_available_for_booking():
            return False, "Номер на ремонте", None
        
        guest = self._find_guest(guest_id)
        if not guest:
            return False, "Гость не найден", None
        
        is_valid, error = validate_date_range(check_in, check_out)
        if not is_valid:
            return False, error, None
        
        booking_id = f"{hotel_id}_{room_number}_{guest_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        booking = Booking(booking_id, hotel_id, room_number, guest_id, check_in, check_out)
        
        if self._check_overlap(booking):
            return False, "Номер уже забронирован на эти даты", None
        
        total_price = self._calculate_price(room, check_in, check_out)
        booking.set_total_price(total_price)
        
        points = int(total_price // 10)
        guest.add_loyalty_points(points)
        
        return True, f"Бронирование успешно создано! Сумма: {total_price}₽, Бонусов начислено: {points}", booking
    
    def cancel_booking(self, booking: Booking) -> bool:
        if booking.get_status() != "active":
            return False
        booking.set_status("cancelled")
        return True
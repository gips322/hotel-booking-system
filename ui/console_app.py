"""Консольное приложение"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repository.json_repo import JsonRepository
from models.hotel import Hotel
from models.guest import Guest
from models.booking import Booking
from models.room import Room
from core.booking_manager import BookingManager  # ← этот менеджер
from core.availability_checker import AvailabilityChecker


class ConsoleApp:
    def __init__(self):
        # ИСПОЛЬЗУЕМ JsonRepository для хранения
        self._hotel_repo = JsonRepository("hotels.json", Hotel)
        self._guest_repo = JsonRepository("guests.json", Guest)
        self._booking_repo = JsonRepository("bookings.json", Booking)
        
        # НО! BookingManager ожидает списки, а не репозитории
        # Поэтому передаем списки из репозиториев
        self._booking_mgr = BookingManager(
            self._hotel_repo.get_all(),  # ← список отелей
            self._guest_repo.get_all(),  # ← список гостей
            self._booking_repo.get_all()  # ← список броней
        )
    
    def run(self):
        while True:
            self._show_main_menu()
            choice = input("\nВаш выбор: ")

            if choice == "1":
                self._manage_hotels()
            elif choice == "2":
                self._manage_rooms()
            elif choice == "3":
                self._manage_guests()
            elif choice == "4":
                self._create_booking()
            elif choice == "5":
                self._cancel_booking()
            elif choice == "6":
                self._show_rooms_status()
            elif choice == "0":
                print("\nДо свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    
    def _show_main_menu(self):
        print("\n" + "=" * 60)
        print("        СИСТЕМА УЧЕТА БРОНИРОВАНИЙ ГОСТИНИЦ")
        print("=" * 60)
        print("1. Управление гостиницами")
        print("2. Управление номерами")
        print("3. Управление гостями")
        print("4. Создать бронирование")
        print("5. Отменить бронирование")
        print("6. Проверить доступность номеров")
        print("0. Выход")
        print("-" * 60)
    
    def _manage_hotels(self):
        while True:
            print("\n--- УПРАВЛЕНИЕ ГОСТИНИЦАМИ ---")
            print("1. Список всех гостиниц")
            print("2. Добавить гостиницу")
            print("3. Удалить гостиницу")
            print("4. Просмотр деталей гостиницы")
            print("5. Назад")
            sub = input("Выбор: ")

            if sub == "1":
                hotels = self._hotel_repo.get_all()
                if not hotels:
                    print("Гостиницы не найдены")
                for h in hotels:
                    print(f"  {h}")

            elif sub == "2":
                hid = input("ID гостиницы: ")
                name = input("Название: ")
                addr = input("Адрес: ")
                try:
                    rating = float(input("Рейтинг (1-5): "))
                    phone = input("Телефон: ")
                    hotel = Hotel(hid, name, addr, rating, phone)
                    if self._hotel_repo.add(hotel):
                        print("✓ Гостиница успешно добавлена")
                    else:
                        print("✗ Гостиница с таким ID уже существует")
                except Exception as e:
                    print(f"✗ Ошибка: {e}")

            elif sub == "3":
                hid = input("ID гостиницы для удаления: ")
                if self._hotel_repo.remove_by_id(hid):
                    print("✓ Гостиница удалена")
                    # Обновляем BookingManager
                    self._booking_mgr = BookingManager(
                        self._hotel_repo.get_all(),
                        self._guest_repo.get_all(),
                        self._booking_repo.get_all()
                    )
                else:
                    print("Гостиница не найдена")

            elif sub == "4":
                hid = input("ID гостиницы: ")
                hotel = self._hotel_repo.get_by_id(hid)
                if hotel:
                    print(f"\n=== {hotel.get_name()} ===")
                    print(f"ID: {hotel.get_id()}")
                    print(f"Адрес: {hotel._address}")
                    print(f"Рейтинг: ★{hotel.get_rating()}")
                    print(f"Телефон: {hotel._phone}")
                    print(f"Всего номеров: {hotel.get_total_rooms()}")
                else:
                    print("Гостиница не найдена")

            elif sub == "5":
                break
    
    def _manage_rooms(self):
        hid = input("Введите ID гостиницы: ")
        hotel = self._hotel_repo.get_by_id(hid)
        if not hotel:
            print("Гостиница не найдена")
            return

        while True:
            print(f"\n--- УПРАВЛЕНИЕ НОМЕРАМИ: {hotel.get_name()} ---")
            print("1. Список всех номеров")
            print("2. Добавить номер")
            print("3. Удалить номер")
            print("4. Изменить цену номера")
            print("5. Назад")
            sub = input("Выбор: ")

            if sub == "1":
                rooms = hotel.get_rooms()
                if not rooms:
                    print("Нет номеров в этой гостинице")
                for r in rooms:
                    print(f"  {r}")

            elif sub == "2":
                rnum = input("Номер комнаты: ")
                price = float(input("Цена за ночь (₽): "))
                cap = int(input("Вместимость (чел.): "))
                floor = int(input("Этаж: "))
                room = Room(rnum, price, cap, [], floor)
                try:
                    hotel.add_room(room)
                    self._hotel_repo.update(hid, hotel)
                    print("✓ Номер успешно добавлен")
                    # Обновляем BookingManager
                    self._booking_mgr = BookingManager(
                        self._hotel_repo.get_all(),
                        self._guest_repo.get_all(),
                        self._booking_repo.get_all()
                    )
                except Exception as e:
                    print(f"✗ Ошибка: {e}")

            elif sub == "3":
                rnum = input("Номер комнаты для удаления: ")
                hotel.remove_room(rnum)
                self._hotel_repo.update(hid, hotel)
                print("✓ Номер удален")
                # Обновляем BookingManager
                self._booking_mgr = BookingManager(
                    self._hotel_repo.get_all(),
                    self._guest_repo.get_all(),
                    self._booking_repo.get_all()
                )

            elif sub == "4":
                rnum = input("Номер комнаты: ")
                for room in hotel.get_rooms():
                    if room.get_room_number() == rnum:
                        new_price = float(input(f"Новая цена (текущая: {room.get_price()}₽): "))
                        room.set_price(new_price)
                        self._hotel_repo.update(hid, hotel)
                        print("✓ Цена обновлена")
                        break
                else:
                    print("Номер не найден")

            elif sub == "5":
                break
    
    def _manage_guests(self):
        while True:
            print("\n--- УПРАВЛЕНИЕ ГОСТЯМИ ---")
            print("1. Список всех гостей")
            print("2. Добавить гостя")
            print("3. Просмотр данных гостя и истории бронирований")
            print("4. Назад")
            sub = input("Выбор: ")

            if sub == "1":
                guests = self._guest_repo.get_all()
                if not guests:
                    print("Гости не найдены")
                for g in guests:
                    print(f"  {g.get_info()}")

            elif sub == "2":
                gid = input("ID гостя: ")
                name = input("ФИО: ")
                contact = input("Телефон: ")
                email = input("Email: ")
                guest = Guest(gid, name, contact, email)
                if self._guest_repo.add(guest):
                    print("✓ Гость успешно добавлен")
                    # Обновляем BookingManager
                    self._booking_mgr = BookingManager(
                        self._hotel_repo.get_all(),
                        self._guest_repo.get_all(),
                        self._booking_repo.get_all()
                    )
                else:
                    print("✗ Гость с таким ID уже существует")

            elif sub == "3":
                gid = input("ID гостя: ")
                guest = self._guest_repo.get_by_id(gid)
                if guest:
                    print("\n" + "=" * 50)
                    print(guest.get_info())
                    print("=" * 50)
                    bookings = [b for b in self._booking_repo.get_all() if b.get_guest_id() == gid]
                    if bookings:
                        print("\nИстория бронирований:")
                        for b in bookings:
                            print(f"  {b}")
                    else:
                        print("\nИстория бронирований пуста")
                else:
                    print("Гость не найден")

            elif sub == "4":
                break
    
    def _create_booking(self):
        print("\n--- СОЗДАНИЕ БРОНИРОВАНИЯ ---")

        hotels = self._hotel_repo.get_all()
        if not hotels:
            print("Нет доступных гостиниц. Сначала добавьте гостиницу.")
            return

        print("\nДоступные гостиницы:")
        for h in hotels:
            print(f"  {h.get_id()} - {h.get_name()}")

        hid = input("\nВведите ID гостиницы: ")
        hotel = self._hotel_repo.get_by_id(hid)
        if not hotel:
            print("Гостиница не найдена")
            return

        print(f"\nНомера в гостинице {hotel.get_name()}:")
        for r in hotel.get_rooms():
            print(f"  {r}")

        rnum = input("\nВведите номер комнаты: ")

        guests = self._guest_repo.get_all()
        if not guests:
            print("Нет зарегистрированных гостей. Сначала добавьте гостя.")
            return

        print("\nЗарегистрированные гости:")
        for g in guests:
            print(f"  {g.get_id()} - {g.get_name()}")

        gid = input("\nВведите ID гостя: ")
        if not self._guest_repo.get_by_id(gid):
            print("Гость не найден")
            return

        check_in = input("Дата заезда (ГГГГ-ММ-ДД): ")
        check_out = input("Дата выезда (ГГГГ-ММ-ДД): ")

        success, message, booking = self._booking_mgr.create_booking(
            hid, rnum, gid, check_in, check_out
        )

        if success and booking:
            self._booking_repo.add(booking)
            # Обновляем BookingManager
            self._booking_mgr = BookingManager(
                self._hotel_repo.get_all(),
                self._guest_repo.get_all(),
                self._booking_repo.get_all()
            )
        print(f"\n{message}")
    
    def _cancel_booking(self):
        print("\n--- ОТМЕНА БРОНИРОВАНИЯ ---")
        bookings = self._booking_repo.get_all()
        active_bookings = [b for b in bookings if b.get_status() == "active"]

        if not active_bookings:
            print("Активных бронирований не найдено")
            return

        print("\nАктивные бронирования:")
        for b in active_bookings:
            print(f"  {b}")

        bid = input("\nВведите ID бронирования для отмены: ")
        booking = self._booking_repo.get_by_id(bid)
        if booking and self._booking_mgr.cancel_booking(booking):
            self._booking_repo.update(bid, booking)
            # Обновляем BookingManager
            self._booking_mgr = BookingManager(
                self._hotel_repo.get_all(),
                self._guest_repo.get_all(),
                self._booking_repo.get_all()
            )
            print("✓ Бронирование отменено")
        else:
            print("Бронирование не найдено")
    
    def _show_rooms_status(self):
        print("\n--- ПРОВЕРКА ДОСТУПНОСТИ НОМЕРОВ ---")
        hid = input("ID гостиницы: ")
        hotel = self._hotel_repo.get_by_id(hid)
        if not hotel:
            print("Гостиница не найдена")
            return

        date = input("Дата (ГГГГ-ММ-ДД): ")

        print(f"\nСтатус номеров в гостинице {hotel.get_name()} на {date}:")
        print("-" * 60)
        for room in hotel.get_rooms():
            free = AvailabilityChecker.is_room_free(room, self._booking_repo.get_all(), date)
            status = "✓ СВОБОДЕН" if free else "✗ ЗАНЯТ"
            print(f"  {room} -> {status}")
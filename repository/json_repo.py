"""JSON репозиторий для работы с файлами"""

import json
import os
from typing import List, TypeVar, Generic, Optional

T = TypeVar('T')


class JsonRepository(Generic[T]):
    def __init__(self, filename: str, entity_class, data_dir: str = "data"):
        self._data_dir = data_dir
        self._filename = filename
        self._entity_class = entity_class
        self._items: List[T] = []
        self._ensure_data_dir()
        self._load()
    
    def _ensure_data_dir(self):
        if not os.path.exists(self._data_dir):
            os.makedirs(self._data_dir)
    
    def _get_filepath(self) -> str:
        return os.path.join(self._data_dir, self._filename)
    
    def _save(self):
        filepath = self._get_filepath()
        data = [item.to_dict() for item in self._items]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load(self):
        filepath = self._get_filepath()
        if not os.path.exists(filepath):
            return
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self._items = [self._entity_class.from_dict(item) for item in data]
    
    def add(self, item: T) -> bool:
        if any(self._get_id(existing) == self._get_id(item) for existing in self._items):
            return False
        self._items.append(item)
        self._save()
        return True
    
    def get_by_id(self, item_id: str) -> Optional[T]:
        for item in self._items:
            if self._get_id(item) == item_id:
                return item
        return None
    
    def get_all(self) -> List[T]:
        return self._items.copy()
    
    def remove_by_id(self, item_id: str) -> bool:
        initial_count = len(self._items)
        self._items = [item for item in self._items if self._get_id(item) != item_id]
        if len(self._items) != initial_count:
            self._save()
            return True
        return False
    
    def update(self, item_id: str, new_item: T) -> bool:
        for i, item in enumerate(self._items):
            if self._get_id(item) == item_id:
                self._items[i] = new_item
                self._save()
                return True
        return False
    
    def clear(self):
        self._items = []
        self._save()
    
    def count(self) -> int:
        return len(self._items)
    
    def _get_id(self, item: T) -> str:
        if hasattr(item, 'get_id'):
            return item.get_id()
        elif hasattr(item, 'get_guest_id'):
            return item.get_guest_id()
        elif hasattr(item, 'get_hotel_id'):
            return item.get_hotel_id()
        elif hasattr(item, 'get_booking_id'):
            return item.get_booking_id()
        elif hasattr(item, 'get_room_number'):
            return item.get_room_number()
        return str(item)
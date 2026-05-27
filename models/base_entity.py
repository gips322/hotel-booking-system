"""Базовый класс для всех сущностей"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any


class BaseEntity(ABC):
    def __init__(self, entity_id: str):
        self._id = entity_id
        self._created_at = datetime.now().isoformat()
        self._updated_at = datetime.now().isoformat()
    
    def get_id(self) -> str:
        return self._id
    
    def update_timestamp(self):
        self._updated_at = datetime.now().isoformat()
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
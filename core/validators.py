"""Функции валидации (чистые функции)"""

from datetime import datetime
from typing import Tuple, Optional


def validate_date_range(check_in: str, check_out: str) -> Tuple[bool, Optional[str]]:
    """
    Проверяет корректность диапазона дат
    
    Returns:
        (is_valid, error_message)
    """
    try:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if check_in_date < today:
            return False, "Дата заезда не может быть в прошлом"
        if check_out_date <= check_in_date:
            return False, "Дата выезда должна быть позже даты заезда"
        return True, None
    except ValueError:
        return False, "Неверный формат даты. Используйте ГГГГ-ММ-ДД"
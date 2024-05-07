from datetime import datetime

from borrowings.models import Borrowing
from payment.models import Payment


FINE_MULTIPLIER = 2


def calculate_borrowing_price(borrowing: Borrowing) -> int:
    days = (borrowing.expected_return_date - datetime.now().date()).days
    return int(days * borrowing.book.daily_fee) * 100


def calculate_fine_price(borrowing: Borrowing):
    if borrowing.actual_return_date and borrowing.actual_return_date > borrowing.expected_return_date:
        days_overdue = (borrowing.actual_return_date - borrowing.expected_return_date).days
        fine_amount = days_overdue * borrowing.book.daily_fee * FINE_MULTIPLIER

        return fine_amount


def params_to_ints(qs):
    """Converts a list of string IDs to a list of integers"""
    return [int(str_id) for str_id in qs.split(",") if str_id]

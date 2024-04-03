FINE_MULTIPLIER = 2


def calculate_fine(borrowing):
    if borrowing.actual_return_date and borrowing.actual_return_date > borrowing.expected_return_date:
        days_overdue = (borrowing.actual_return_date - borrowing.expected_return_date).days
        fine_amount = days_overdue * borrowing.book.daily_fee * FINE_MULTIPLIER

        return fine_amount


def params_to_ints(qs):
    """Converts a list of string IDs to a list of integers"""
    return [int(str_id) for str_id in qs.split(",") if str_id]

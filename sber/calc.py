from datetime import datetime
from dateutil.relativedelta import relativedelta


def calculate_percents(data):
    date = extract_date(data)
    periods = extract_periods(data)
    amount = extract_amount(data)
    rate = extract_rate(data)

    coff = 1 + (rate / 12) / 100
    expected_amount = amount
    result = {}
    for i in range(periods):
        expected_amount = expected_amount * coff
        cur_date = (date + relativedelta(months=i)).strftime('%d.%m.%Y')
        rounded = round(expected_amount, 2)
        result[cur_date] = rounded
    return result


def extract_date(data):
    date_text = data.get('date')
    if date_text is None or not isinstance(date_text, str):
        raise ValueError("Missing or invalid 'date'")
    try:
        date = datetime.strptime(date_text, '%d.%m.%Y')
        return date
    except ValueError:
        raise ValueError("Invalid date format. Expected format: dd.mm.yyyy")


def extract_periods(data):
    periods = data.get('periods')
    if periods is None or not isinstance(periods, int):
        raise ValueError("Missing or invalid 'periods'")
    if periods < 1 or periods > 60:
        raise ValueError("'periods' values must be between 1 and 60")
    return periods


def extract_amount(data):
    amount = data.get('amount')
    if amount is None or not isinstance(amount, int):
        raise ValueError("Missing or invalid 'amount'")
    if amount < 10_000 or amount > 3_000_000:
        raise ValueError("'amount' values must be between 10000 and 3000000")
    return amount


def extract_rate(data):
    rate = data.get('rate')
    if rate is None or not (isinstance(rate, float) or isinstance(rate, int)):
        raise ValueError("Missing or invalid 'rate'")
    if rate < 1 or rate > 8:
        raise ValueError("'rate' values must be between 1 and 8")
    return rate

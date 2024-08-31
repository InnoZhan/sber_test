import pytest
from copy import deepcopy
from sber import calc


def test_calculate_percents():
    data = {
        'date': '31.01.2021',
        'periods': 12,
        'amount': 10000,
        'rate': 6,
    }

    assert calc.calculate_percents(data) == {
        '31.01.2021': 10050.0,
        '28.02.2021': 10100.25,
        '31.03.2021': 10150.75,
        '30.04.2021': 10201.51,
        '31.05.2021': 10252.51,
        '30.06.2021': 10303.78,
        '31.07.2021': 10355.29,
        '31.08.2021': 10407.07,
        '30.09.2021': 10459.11,
        '31.10.2021': 10511.4,
        '30.11.2021': 10563.96,
        '31.12.2021': 10616.78,
    }

    no_date = deepcopy(data)
    del no_date['date']
    with pytest.raises(ValueError) as excinfo:
        calc.calculate_percents(no_date)
    assert "Missing or invalid 'date'" in str(excinfo.value)

    no_date = deepcopy(data)
    del no_date['rate']
    with pytest.raises(ValueError) as excinfo:
        calc.calculate_percents(no_date)
    assert "Missing or invalid 'rate'" in str(excinfo.value)

    no_date = deepcopy(data)
    del no_date['periods']
    with pytest.raises(ValueError) as excinfo:
        calc.calculate_percents(no_date)
    assert "Missing or invalid 'periods'" in str(excinfo.value)

    no_date = deepcopy(data)
    del no_date['amount']
    with pytest.raises(ValueError) as excinfo:
        calc.calculate_percents(no_date)
    assert "Missing or invalid 'amount'" in str(excinfo.value)


def test_extract_date():
    dt = calc.extract_date({'date': '31.01.2021'})

    assert str(dt) == '2021-01-31 00:00:00'

    with pytest.raises(ValueError) as excinfo:
        calc.extract_date({})
    assert "Missing or invalid 'date'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_date({'date': 1})
    assert "Missing or invalid 'date'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_date({'date': '2021-01-31 00:00:00'})
    assert "Invalid date format. Expected format: dd.mm.yyyy" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_date({'date': '32.01.2021'})
    assert "Invalid date format. Expected format: dd.mm.yyyy" in str(excinfo.value)


def test_extract_periods():
    periods = calc.extract_periods({'periods': 1})
    assert periods == 1

    periods = calc.extract_periods({'periods': 60})
    assert periods == 60

    with pytest.raises(ValueError) as excinfo:
        calc.extract_periods({})
    assert "Missing or invalid 'periods'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_periods({'periods': '1'})
    assert "Missing or invalid 'periods'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_periods({'periods': 1.0})
    assert "Missing or invalid 'periods'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_periods({'periods': 0})
    assert "'periods' values must be between 1 and 60" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_periods({'periods': 61})
    assert "'periods' values must be between 1 and 60" in str(excinfo.value)


def test_extract_amount():
    amount = calc.extract_amount({'amount': 10_000})
    assert amount == 10_000

    amount = calc.extract_amount({'amount': 3_000_000})
    assert amount == 3_000_000

    with pytest.raises(ValueError) as excinfo:
        calc.extract_amount({})
    assert "Missing or invalid 'amount'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_amount({'amount': None})
    assert "Missing or invalid 'amount'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_amount({'amount': 1.0})
    assert "Missing or invalid 'amount'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_amount({'amount': 9_999})
    assert "'amount' values must be between 10000 and 3000000" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_amount({'amount': 3_000_001})
    assert "'amount' values must be between 10000 and 3000000" in str(excinfo.value)


def test_extract_rate():
    rate = calc.extract_rate({'rate': 1})
    assert rate == 1

    rate = calc.extract_rate({'rate': 8})
    assert rate == 8

    rate = calc.extract_rate({'rate': 1.0})
    assert rate == 1.0

    rate = calc.extract_rate({'rate': 8.0})
    assert rate == 8.0

    with pytest.raises(ValueError) as excinfo:
        calc.extract_rate({})
    assert "Missing or invalid 'rate'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_rate({'rate': None})
    assert "Missing or invalid 'rate'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_rate({'rate': '1'})
    assert "Missing or invalid 'rate'" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_rate({'rate': 0.9})
    assert "'rate' values must be between 1 and 8" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calc.extract_rate({'rate': 8.1})
    assert "'rate' values must be between 1 and 8" in str(excinfo.value)

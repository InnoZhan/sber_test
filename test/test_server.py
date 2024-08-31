def test_index(client):
    # Test for valid request and valid response
    response = client.get('/', json={
        'date': '31.01.2021',
        'periods': 12,
        'amount': 10000,
        'rate': 6,
    })
    assert response.status_code == 200
    assert response.json == {
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


def test_bad_request(client):
    # Test for bad json
    bad_data = "{bad_json: true}"
    response = client.get('/', data=bad_data, content_type='application/json')
    assert response.status_code == 400
    assert response.json == {'error': 'Json format is not valid'}


def test_server_error(client):
    # Test for not json data passed
    response = client.get('/')
    assert response.status_code == 400
    assert response.json == {'error': 'Application required json to be passed'}


def test_other_route(client):
    # Test for wrong route is called
    response = client.get('/index', json={
        'date': '31.01.2021',
        'periods': 12,
        'amount': 10000,
        'rate': 6,
    })
    assert response.status_code == 404
    assert response.json == {'error': 'No such endpoint'}


def test_bad_data(client):
    # Test for valid json but wrong data format
    response = client.get('/', json={
        'date': '31.01.2021',
        'periods': 12,
        'amount': 9900,
        'rate': 6,
    })
    assert response.status_code == 400
    assert response.json == {'error': "'amount' values must be between 10000 and 3000000"}


def test_internal_server_error(client, monkeypatch):
    def mock_calculate_percents(data):
        raise Exception("Simulated server error")

    monkeypatch.setattr('sber.calc.calculate_percents', mock_calculate_percents)

    valid_json = {
        "date": "01.01.2022",
        "periods": 12,
        "amount": 100000,
        "rate": 5
    }
    response = client.get('/', json=valid_json)
    assert response.status_code == 500
    assert response.json == {'error': 'Internal server error'}

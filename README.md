# Deposit calculator service 

This project is a test assignment for Sberbank interview. Flask application dedicated to calculate earnings for deposit with provided deposit period length, deposited amount and interest rate

## Installation

1. Clone the repository:
```shell
git clone https://github.com/InnoZhan/sber_test.git
cd sber_test
```

## Usage

1. Build docker image and run container:
```shell
docker build -t sber_test .
docker run -p 8000:8000 sber_test
```

2. The application will start and be accessible at http://127.0.0.1:8000.

## Running Tests

We use pytest for running tests. Ensure you have the test requirements installed:

```shell
pip install pytest pytest-cov
pytest --cov=sber --cov-report=term-missing
coverage html
```
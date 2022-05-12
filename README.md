# countries-rest-api

REST API created using FastAPI and SQLite3 with a simple countries record database ✌️  
I am well aware of SQLAlchemy, however I wanted to implement the functions to interact with the database myself for educational purposes.

## Endpoints

![endpoints](https://user-images.githubusercontent.com/88138099/165749658-d1c6b224-fd55-4adf-895c-b48f6ae3e2bd.png)

## Installation

Begin by cloning the repository:

```bash
git clone https://github.com/dsymbol/countries-rest-api
```

There are two ways to begin using the api, depending on your preference:

### Manual

```bash
pip install -r requirements.txt
python utils/build_database.py
python -m uvicorn --port 5000 server:app
```

### Docker

```bash
docker build -t countries-rest-api .
docker run --name countries-rest-api -p 5000:5000 countries-rest-api:latest
```

You can view the API docs by visiting http://127.0.0.1:5000

## PyTest

Tests are independent of each other, database must be reset after every test file ran.

**Example**

```bash
python3 utils/build_database.py
python3 -m uvicorn --port 5000 server:app
python3 -m pytest tests/test_create_country.py
```

from json import load
from typing import Optional

import uvicorn
from fastapi import FastAPI, status
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from utils import database_helper as db
from utils import scrape_data

app = FastAPI(docs_url="/", redoc_url=None, title="countries-rest-api")


def my_schema():
    if app.openapi_schema:
        return app.openapi_schema

    with open(f'data/model.json', 'r') as f:
        data = load(f)

    openapi_schema = get_openapi(
        title="countries-rest-api",
        description="REST API created using FastAPI and SQLite3 with a simple countries record database",
        contact={"name": "dsymbol", "url": "http://github.com/dsymbol/countries-rest-api"},
        version="1.0",
        routes=app.routes,
    )
    openapi_schema["components"] = data["components"]
    openapi_schema["paths"] = data["paths"]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = my_schema


def replace_with_space(name):
    if "+" in name:
        name = name.replace("+", " ")
    if "-" in name:
        name = name.replace("+", " ")
    return name


@app.get("/api/country", tags=["Country"])
def read_all_countries():
    result = db.get_all_countries()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@app.get("/api/country/population", tags=["Country"])
def read_by_population(gt: int = None, lt: int = None):
    result = db.get_all_countries(gt, lt)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@app.get("/api/country/{name}", tags=["Country"])
def read_by_name(name: str):
    name = replace_with_space(name)
    result = db.get_country(name=name)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "Could not find a country with that name"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@app.post("/api/country/{name}", tags=["Country"])
def create_country(name: str, payload: dict):
    name = replace_with_space(name)
    name = scrape_data.validate_country_name(name)
    if not name:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": "Invalid or non "
                                                                                                  "existent country "
                                                                                                  "name: refer to "
                                                                                                  "data/country_list.txt"})
    result = db.get_country(name=name)
    if result:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={"message": "Country already exists"})
    payload.update(dict(population=scrape_data.scrape_population(name)))
    result, errors = db.create_country(name, payload)
    if not result:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": errors})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": 'Country created'})


@app.delete("/api/country/{name}", tags=["Country"])
def read_by_name(name: str):
    name = replace_with_space(name)
    result = db.get_country(name)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Found"})
    db.delete_country(name=name)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": 'Country deleted'})


@app.put("/api/country/{name}", tags=["Country"])
def update_country(name: str, payload: Optional[dict] = {}):
    name = replace_with_space(name)
    name = scrape_data.validate_country_name(name)
    if not name:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": "Invalid or non "
                                                                                                  "existent country "
                                                                                                  "name: refer to "
                                                                                                  "data/country_list.txt"})
    result = db.get_country(name=name)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "Could not find a country with that name"})
    payload.update(dict(population=scrape_data.scrape_population(name)))
    result, errors = db.update_country(name, payload)
    if not result:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": errors})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": 'Country updated'})


@app.get("/api/capital/{capital}", tags=["Country"])
def read_by_capital(capital: str):
    capital = replace_with_space(capital)
    result = db.get_country(capital=capital)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "Could not find a country with that capital"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@app.get("/api/language/{language}", tags=["Country"])
def read_by_language(language: str):
    result = db.get_country(language=language)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "Could not find a country with that language"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@app.get("/api/currency/{currency}", tags=["Country"])
def read_by_currency(currency: str):
    result = db.get_country(currency=currency)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "Could not find a country with that currency"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=5000, log_level="info", reload=True)

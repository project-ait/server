import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from core.sql_util import check_and_create_table
from oauth import auth
from service.subway import subway
from service.summary import summary
from service.weather import weather

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(weather.router, prefix="/service/weather", tags=["weather"])
app.include_router(summary.router, prefix="/service/summary", tags=["summary"])
app.include_router(subway.router, prefix="/service/subway", tags=["subway"])

check_and_create_table()


@app.get("/")
def root():
    return {"message": "AIT server is running!"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=1777, reload=True)

    if not os.path.exists(".env"):
        print(
            "ENV >> Cannot found .env file, use pre-configured environment variables."
        )
        print(
            "ENV >> If not prepared environment variables, server will be throw exception."
        )
    else:
        print("ENV >> Found .env file! load environment variables from .env file.")
        load_dotenv()

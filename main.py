import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from core.sql_util import check_and_create_table
from routers import deepl, location, subway, summary, weather, auth

# from service.summary.nlp_util import update_nlp_client

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(weather.router, prefix="/service/weather", tags=["weather"])
app.include_router(summary.router, prefix="/service/summary", tags=["summary"])
app.include_router(subway.router, prefix="/service/subway", tags=["subway"])
app.include_router(deepl.router, prefix="/service/deepl", tags=["deepl"])
app.include_router(location.router, prefix="/service/location", tags=["ipinfo"])

check_and_create_table()


@app.get("/")
def root():
    return {"message": "AIT server is running!"}


if __name__ == "__main__":
    print("ENV >> Check .env file...")
    if not os.path.exists(".env"):
        print("""
            ENV >> Cannot found .env file, use pre-configured environment variables.
            ENV >> If not prepared environment variables, server will be throw exception.
            """)
    else:
        print("ENV >> DotEnv File Found! load environment variables from .env file.")
        load_dotenv()
        # update_nlp_client()

    uvicorn.run("main:app", port=1777, reload=True)

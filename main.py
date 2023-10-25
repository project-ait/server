import uvicorn
from fastapi import FastAPI

from core.sql_util import check_and_create_table
from oauth import auth
from service.weather import weather

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(weather.router, prefix="/service/weather")

check_and_create_table()


@app.get("/")
def root():
    return {"message": "AIT server is running!"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=1777, reload=True)

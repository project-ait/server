import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

app = FastAPI()

# app.include_router(file.router, prefix="/file", tags=["file"])


@app.get("/")
def root():
    return {"message": "AIT server is running!"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=1777, reload=True)
import uvicorn
from fastapi import FastAPI

from auth import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
def root():
    return {"message": "AIT server is running!"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=1777, reload=True)

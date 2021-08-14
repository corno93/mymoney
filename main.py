import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from constants import DATA_DIR, DATA_FILE
from views import router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)


@app.on_event("startup")
def startup_event():
    # this event should be blocking as we need the DATA_FILE to exist before anything can happen
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w").close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

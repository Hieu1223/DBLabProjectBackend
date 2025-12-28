from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app import STORAGE_DIR

app = FastAPI()

app.mount(
    "/files",
    StaticFiles(directory=STORAGE_DIR),
    name="files"
)

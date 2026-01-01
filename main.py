from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app import STORAGE_DIR
from app import router
app = FastAPI()

app.mount(
    "/files",
    StaticFiles(directory=STORAGE_DIR),
    name="files"
)


app.include_router(router)


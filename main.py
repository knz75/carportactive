from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def index():
    return FileResponse("static/index.html")

app.mount("/", StaticFiles(directory="static"), name="static")
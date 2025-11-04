from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .orm import init_db
from .api import router as api_router
from .pages import router as pages_router

app = FastAPI(title="API Cursos")

init_db()

# Archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)
app.include_router(pages_router)


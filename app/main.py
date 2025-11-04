from fastapi import FastAPI
from .orm import init_db
from .api import router

app = FastAPI(title="API Cursos")

init_db()

app.include_router(router)


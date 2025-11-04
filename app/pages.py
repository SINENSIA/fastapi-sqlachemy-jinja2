from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from typing import Optional
from sqlalchemy.orm import Session
from .deps import get_db
from .models import CursoIn, CursoOut
from .orm import CursoORM
from datetime import date

router = APIRouter(tags=["pages"])  # sin prefix: raíz del sitio

templates = Jinja2Templates(directory="templates")

@router.get("/")
def home():
    # 302/307 redirigen a otra URL. Usamos 302 por simplicidad.
    return RedirectResponse(url="/cursos", status_code=status.HTTP_302_FOUND)

@router.get("/cursos")
def cursos_list(request: Request, db: Session = Depends(get_db)):
    cursos = db.query(CursoORM).all()
    return templates.TemplateResponse("cursos_list.html", {"request": request, "cursos": cursos})

@router.get("/cursos/nuevo")
def cursos_new_form(request: Request):
    return templates.TemplateResponse("cursos_new.html", {"request": request})

@router.post("/cursos/nuevo")
def cursos_new_submit(
    request: Request,
    nombre: str = Form(...),               # Form(...) => vendrá del form HTML
    descripcion: Optional[str] = Form(None),
    duracion_horas: int = Form(...),
    inicio: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        inicio_dt = date.fromisoformat(inicio.strip())
        data = CursoIn(
            nombre=nombre,
            descripcion=descripcion,
            duracion_horas=int(duracion_horas),
            inicio=inicio_dt,
        )
    except Exception as e:
        # Re-render de la vista con el error
        return templates.TemplateResponse(
            "cursos_new.html",
            {"request": request, "error": str(e)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Guardar en BD
    c = CursoORM(**data.model_dump())
    db.add(c)
    db.commit()
    # 303 SEE_OTHER: tras un POST, indica al cliente que debe realizar un GET
    # a la URL indicada. Evita re-envío del formulario al refrescar.
    return RedirectResponse(url="/cursos", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/cursos/{curso_id}/editar")
def cursos_edit_form(request: Request, curso_id: int, db: Session = Depends(get_db)):
    c = db.get(CursoORM, curso_id)
    if not c:
        raise HTTPException(404, "No encontrado")
    return templates.TemplateResponse("cursos_edit.html", {"request": request, "curso": c})

@router.post("/cursos/{curso_id}/editar")
def cursos_edit_submit(
    request: Request,
    curso_id: int,
    nombre: str = Form(...),
    descripcion: Optional[str] = Form(None),
    duracion_horas: int = Form(...),
    inicio: str = Form(...),
    db: Session = Depends(get_db),
):
    c = db.get(CursoORM, curso_id)
    if not c:
        raise HTTPException(404, "No encontrado")

    try:
        inicio_dt = date.fromisoformat(inicio.strip())
        data = CursoIn(
            nombre=nombre,
            descripcion=descripcion,
            duracion_horas=int(duracion_horas),
            inicio=inicio_dt,
        )
    except Exception as e:
        return templates.TemplateResponse(
            "cursos_edit.html",
            {"request": request, "curso": c, "error": str(e)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    for k, v in data.model_dump().items():
        setattr(c, k, v)
    db.commit()
    return RedirectResponse(url="/cursos", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/cursos/{curso_id}/borrar")
def cursos_delete(curso_id: int, db: Session = Depends(get_db)):
    c = db.get(CursoORM, curso_id)
    if c:
        db.delete(c)
        db.commit()
    return RedirectResponse(url="/cursos", status_code=status.HTTP_303_SEE_OTHER)

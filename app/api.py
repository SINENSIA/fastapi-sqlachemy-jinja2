from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .models import CursoIn, CursoOut
from .deps import get_db
from .orm import CursoORM

router = APIRouter(prefix="/api", tags=["cursos"])

@router.post("/cursos", response_model=CursoOut, status_code=status.HTTP_201_CREATED)
def crear_curso(data: CursoIn, db: Session = Depends(get_db)):
    curso = CursoORM(
        nombre=data.nombre,
        descripcion=data.descripcion,
        duracion_horas=data.duracion_horas,
        inicio=data.inicio,
    )
    db.add(curso)
    db.commit()
    db.refresh(curso)

    return CursoOut(
        id=curso.id,
        nombre=curso.nombre,
        descripcion=curso.descripcion,
        duracion_horas=curso.duracion_horas,
        inicio=curso.inicio,
    )

@router.get("/cursos", response_model=List[CursoOut])
def listas_cursos(db: Session = Depends(get_db)):
    cursos = db.query(CursoORM).all()
    return [
        CursoOut(id=curso.id, nombre=curso.nombre, descripcion=curso.descripcion, duracion_horas=curso.duracion_horas, inicio=curso.inicio)
        for curso in cursos
    ]

@router.get("/cursos/{curso_id}", response_model=CursoOut)
def obtener_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.get(CursoORM, curso_id)
    if not curso:
        raise HTTPException(404, "Curso no encontrado")
    return CursoOut(id=curso.id, nombre=curso.nombre, descripcion=curso.descripcion, deracion_horas=curso.duracion_horas, inicio=curso.inicio)

@router.put("/cursos/{curso_id}", response_model=CursoOut)
def actualizar_curso(curso_id: int, data: CursoIn, db: Session = Depends(get_db)):
    curso = db.get(CursoORM, curso_id)
    if not curso:
        raise HTTPException(404, "No encontrado")
    for k, v in data.model_dump().items():
        setattr(curso, k, v)
    db.commit()
    db.refresh(curso)
    return CursoOut(id=curso.id, nombre=curso.nombre, descripcion=curso.descripcion,
                    duracion_horas=curso.duracion_horas, inicio=curso.inicio)

# 204 si está vacio
@router.delete("/cursos/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.get(CursoORM, curso_id)
    if not curso:
        raise HTTPException(404, "No encontrado")
    db.delete(curso)
    db.commit()
    
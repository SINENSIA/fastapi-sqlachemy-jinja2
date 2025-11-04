from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import date

class CursoIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str
    descripcion: Optional[str] = None
    duracion_horas: int = Field(ge=1, le=500)
    inicio: Optional[date] = None

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, value: str):
        if not value:
            raise ValueError("EL nombre es obligatorio")
        return value

class CursoOut(CursoIn):
    id: int

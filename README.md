# FastAPI SQLAlchemy Jinja2

Aplicación de ejemplo que combina FastAPI, SQLAlchemy y plantillas Jinja2 para gestionar cursos mediante una API REST y una interfaz web.

## Requisitos
- Python 3.10 o superior
- `pip` para instalar dependencias

Se recomienda usar un entorno virtual para aislar las dependencias del proyecto.

## Instalación
```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows usa: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecución del servidor
```bash
uvicorn app.main:app --reload
```

El parámetro `--reload` recarga el servidor automáticamente al detectar cambios. Una base de datos SQLite (`demo.db`) se crea en la raíz del proyecto la primera vez que inicia la aplicación.

## Interfaz web
- Listado de cursos: http://127.0.0.1:8000/cursos
- Alta de curso: http://127.0.0.1:8000/cursos/nuevo
- Edición/Borrado: disponible desde el listado.

Los formularios guardan la información directamente en la base de datos mediante SQLAlchemy.

## API REST
La misma información está disponible mediante endpoints JSON bajo el prefijo `/api`.

| Método | Ruta                 | Descripción                    |
|--------|----------------------|--------------------------------|
| GET    | `/api/cursos`        | Lista todos los cursos.        |
| POST   | `/api/cursos`        | Crea un curso nuevo.           |
| GET    | `/api/cursos/{id}`   | Obtiene un curso por su ID.    |
| PUT    | `/api/cursos/{id}`   | Actualiza un curso existente.  |
| DELETE | `/api/cursos/{id}`   | Elimina un curso.              |

### Ejemplo de petición POST
```bash
curl -X POST http://127.0.0.1:8000/api/cursos \
  -H "Content-Type: application/json" \
  -d '{
        "nombre": "FastAPI desde cero",
        "descripcion": "Curso introductorio",
        "duracion_horas": 12,
        "inicio": "2025-01-15"
      }'
```

## Base de datos
La configuración por defecto usa SQLite (`sqlite:///./demo.db`). Cambia `DATABASE_URL` en `app/orm.py` si necesitas otro motor o ubicación de la base de datos.

## Pruebas
```bash
pytest
```

Actualmente no se incluyen tests, pero el comando sirve como punto de partida para añadirlos.

## Estructura principal
- `app/main.py`: punto de entrada de FastAPI.
- `app/api.py`: rutas REST.
- `app/pages.py`: vistas y formularios Jinja2.
- `app/orm.py`: modelos e inicialización de SQLAlchemy.
- `templates/`: plantillas HTML.
- `static/`: recursos estáticos (CSS, JS, etc.).

## Contribuciones
1. Crea una rama con tu cambio.
2. Asegúrate de que la aplicación inicia correctamente y, si añades tests, que pasen con `pytest`.
3. Envía un pull request describiendo el cambio y cómo probarlo.


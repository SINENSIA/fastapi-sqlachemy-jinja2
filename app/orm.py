from sqlalchemy import create_engine, Integer, String, Text, Date, Column
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./demo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CursoORM(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    duracion_horas = Column(Integer, nullable=False)
    inicio = Column(Date, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)
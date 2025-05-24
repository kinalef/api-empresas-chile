from sqlalchemy import Column, Integer, String, Date
from app.db import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, index=True)
    razon_social = Column(String)
    fecha_actuacion = Column(String)  # luego puedes convertirlo a Date si es necesario
    fecha_registro = Column(String)
    fecha_aprobacion_sii = Column(String)
    anio = Column(Integer)
    mes = Column(String)
    comuna_tributaria = Column(String)
    region_tributaria = Column(String)
    codigo_sociedad = Column(String)
    tipo_actuacion = Column(String)
    capital = Column(Integer)
    comuna_social = Column(String)
    region_social = Column(String)
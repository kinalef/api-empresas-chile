from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_ , func
from app.db import SessionLocal
from app.models import Empresa
from app.schemas import EmpresaOut, EmpresasPaginatedOut
from typing import List, Optional


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "API Empresas Chile 🇨🇱",
        "descripcion": "Esta API entrega acceso a información estructurada del Registro de Empresas y Sociedades (RES) de Chile, incluyendo filtros, estadísticas y exploración por ID.",
        "documentacion": "https://api-empresas-chile.onrender.com/docs",
        "github": "https://github.com/tu_usuario/api-empresas-chile",
        "dataset_original": "https://datos.gob.cl/dataset/registro-de-empresas-y-sociedades"
    }

@router.get(
    "/empresas",
    response_model=EmpresasPaginatedOut,
    summary="Listar empresas con filtros opcionales y paginación",
    description="""
Este endpoint permite obtener una lista paginada de empresas registradas. Puedes:

- Obtener todas las empresas: `GET /empresas`
- Controlar la paginación: `GET /empresas?skip=0&limit=10`
- Filtrar por comuna: `GET /empresas?comuna=PROVIDENCIA`
- Filtrar por año: `GET /empresas?anio=2013`
- Buscar por palabra clave en razón social: `GET /empresas?razon=transporte`
- Combinar filtros: `GET /empresas?comuna=MAIPU&razon=transporte&anio=2013&limit=10&skip=20`
"""
)
def listar_empresas(
    skip: int = Query(
        0,
        ge=0,
        description="Número de registros a omitir (paginación)"
    ),
    limit: int = Query(
        20,
        le=100,
        description="Número máximo de registros a retornar"
    ),
    razon: Optional[str] = Query(
        None,
        description="Buscar en la razón social (parcial, sin distinción de mayúsculas)",
        examples={"ejemplo": {"summary": "Buscar 'transporte'", "value": "transporte"}}
    ),
    comuna: Optional[str] = Query(
        None,
        description="Filtrar por comuna tributaria (ej: PROVIDENCIA)",
        examples={"ejemplo": {"summary": "Filtrar por comuna", "value": "SANTIAGO"}}
    ),
    anio: Optional[int] = Query(
        None,
        description="Filtrar por año de constitución",
        examples={"ejemplo": {"summary": "Filtrar por año", "value": 2013}}
    ),
    db: Session = Depends(get_db)
):
    query = db.query(Empresa)

    if razon:
        query = query.filter(Empresa.razon_social.ilike(f"%{razon}%"))
    if comuna:
        query = query.filter(Empresa.comuna_tributaria.ilike(comuna))
    if anio:
        query = query.filter(Empresa.anio == anio)
    
    total = query.count()
    empresas = query.offset(skip).limit(limit).all()
    empresas_out = [EmpresaOut.model_validate(e) for e in empresas]

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": empresas_out
    }

@router.get(
    "/estadisticas",
    summary="Estadísticas globales de empresas",
    description="""
Este endpoint entrega estadísticas globales de las empresas registradas, incluyendo:

- Total de empresas por año
- Total de empresas por comuna tributaria
- Total de empresas por rangos de capital

Puedes usar el parámetro opcional `anio` para filtrar los resultados por un año específico.
    """
)
def estadisticas_globales(anio: int = Query(None, description="Filtrar estadísticas por año específico"), db: Session = Depends(get_db)):
    filtros = []
    if anio:
        filtros.append(Empresa.anio == anio)

    # Por año (si no se filtra)
    if anio:
        empresas_por_anio = {str(anio): db.query(Empresa).filter(*filtros).count()}
    else:
        empresas_por_anio = {
            str(a): t for a, t in db.query(Empresa.anio, func.count(Empresa.id))
            .group_by(Empresa.anio).order_by(Empresa.anio).all()
        }

    # Por comuna tributaria
    query_comuna = db.query(Empresa.comuna_tributaria, func.count(Empresa.id))
    if filtros:
        query_comuna = query_comuna.filter(*filtros)
    empresas_por_comuna = {
        comuna: total for comuna, total in query_comuna
        .group_by(Empresa.comuna_tributaria)
        .order_by(func.count(Empresa.id).desc())
        .all()
    }

    # Por rango de capital
    rangos = {
        "menos_de_1m": (0, 999_999),
        "entre_1m_y_10m": (1_000_000, 10_000_000),
        "mas_de_10m": (10_000_001, None),
    }
    resultados_rangos = {}
    for etiqueta, (minimo, maximo) in rangos.items():
        query = db.query(func.count(Empresa.id)).filter(Empresa.capital >= minimo)
        if maximo:
            query = query.filter(Empresa.capital <= maximo)
        if filtros:
            query = query.filter(*filtros)
        resultados_rangos[etiqueta] = query.scalar()

    return {
        "por_anio": empresas_por_anio,
        "por_comuna": empresas_por_comuna,
        "por_rango_capital": resultados_rangos
    }

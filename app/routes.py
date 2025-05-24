from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
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

    @router.get("/empresas/{id}", response_model=EmpresaOut, summary="Obtener una empresa por ID")
    def obtener_empresa_por_id(id: int, db: Session = Depends(get_db)):
        empresa = db.query(Empresa).filter(Empresa.id == id).first()
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")
        return empresa
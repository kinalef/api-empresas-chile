from pydantic import BaseModel
from typing import List, Optional

class EmpresaOut(BaseModel):
    id: int
    rut: str
    razon_social: str
    fecha_actuacion: str
    fecha_registro: str
    fecha_aprobacion_sii: str
    anio: int
    mes: str
    comuna_tributaria: str
    region_tributaria: str
    codigo_sociedad: str
    tipo_actuacion: str
    capital: int
    comuna_social: str
    region_social: str

    class Config:
        from_attributes = True



class EmpresasPaginatedOut(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[EmpresaOut]
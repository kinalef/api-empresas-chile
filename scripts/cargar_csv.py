import os
import csv
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Empresa
from app.schemas import EmpresaOut
from pathlib import Path


def cargar_empresas_desde_archivo(filepath, db: Session):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            empresa = Empresa(
                rut=row['RUT'],
                razon_social=row['Razon Social'],
                fecha_actuacion=row['Fecha de actuacion (1era firma)'],
                fecha_registro=row['Fecha de registro (ultima firma)'],
                fecha_aprobacion_sii=row['Fecha de aprobacion x SII'],
                anio=int(row['Anio']),
                mes=row['Mes'],
                comuna_tributaria=row['Comuna Tributaria'],
                region_tributaria=row['Region Tributaria'],
                codigo_sociedad=row['Codigo de sociedad'],
                tipo_actuacion=row['Tipo de actuacion'],
                capital=int(row['Capital']),
                comuna_social=row['Comuna Social'],
                region_social=row['Region Social']
            )
            db.add(empresa)
        db.commit()
        print(f"✔️ {filepath.name} cargado exitosamente.")

def cargar_todos_los_csv():
    db = SessionLocal()
    data_dir = Path("data")
    archivos = sorted(data_dir.glob("*.csv"))

    if not archivos:
        print("⚠️ No se encontraron archivos CSV en la carpeta data/")
        return

    for archivo in archivos:
        print(f"📂 Cargando: {archivo.name}")
        cargar_empresas_desde_archivo(archivo, db)

    db.close()

if __name__ == "__main__":
    cargar_todos_los_csv()
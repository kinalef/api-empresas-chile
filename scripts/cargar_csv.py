import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from sqlalchemy.orm import Session
from app.models import Empresa
from app.db import SessionLocal

CSV_PATH = os.path.join("data", "2013-sociedades-por-fecha-rut-constitucion.csv")

def cargar_empresas():
    db: Session = SessionLocal()

    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        empresas = []
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
                capital=int(row['Capital']) if row['Capital'].isdigit() else 0,
                comuna_social=row['Comuna Social'],
                region_social=row['Region Social'],
            )
            empresas.append(empresa)

        db.bulk_save_objects(empresas)
        db.commit()
        print(f"{len(empresas)} empresas cargadas correctamente.")

if __name__ == "__main__":
    cargar_empresas()
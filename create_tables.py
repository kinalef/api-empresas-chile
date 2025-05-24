from app.db import Base, engine
from app.models import Empresa

print("Creando tablas...")
Base.metadata.create_all(bind=engine)
print("¡Listo!")
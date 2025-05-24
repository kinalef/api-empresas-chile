
# API Empresas Chile 🇨🇱

API REST construida con **FastAPI** y **PostgreSQL** para exponer información del Registro de Empresas y Sociedades (RES) de Chile.

## 🔍 ¿Qué hace esta API?

> 🗂️ Los datos provienen del [Registro de Empresas y Sociedades (RES)](https://datos.gob.cl/dataset/registro-de-empresas-y-sociedades), disponibles públicamente en el portal Datos.gob.cl.

- Carga datos desde archivos CSV públicos del RES
- Expone endpoints REST con:
  - Listado paginado de empresas
  - Filtros por razón social, comuna y año
  - Detalle de empresa por ID
  - Estadísticas agregadas por año, comuna y rango de capital
- Documentación automática vía Swagger

## 🚀 Cómo ejecutar localmente

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/api-empresas-chile.git
cd api-empresas-chile
```

2. Crea y activa un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
```

4. Crea una base de datos PostgreSQL y configura `.env`:

```bash
cp .env.example .env
# Edita los valores con tus credenciales
```

5. Crea las tablas y carga datos desde todos los archivos CSV de la carpeta `data/` (opcional):

```bash
python create_tables.py
python -m scripts.cargar_csv
```

6. Corre la API:

```bash
uvicorn app.main:app --reload
```

Abre [http://localhost:8000/docs](http://localhost:8000/docs) para ver la documentación Swagger.

## 🗂️ Estructura del proyecto

```
.
├── app/               # Código principal de la API (modelos, rutas, etc.)
├── scripts/           # Scripts de carga desde CSV
├── data/              # CSV con datos del RES (no se sube)
├── .env.example       # Variables de entorno
├── requirements.txt   # Dependencias
└── README.md          # Esta documentación
```

## 📦 Dependencias clave

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [psycopg2](https://pypi.org/project/psycopg2/)
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/)

## 📝 Licencia

Este proyecto se encuentra disponible públicamente con fines educativos y de portafolio personal. Puedes explorarlo, aprender y reutilizar ideas libremente.

## 🌐 API en línea

La API está desplegada en Render y disponible públicamente en:

🔗 https://api-empresas-chile.onrender.com

Accede a la documentación Swagger aquí:  
📘 [https://api-empresas-chile.onrender.com/docs](https://api-empresas-chile.onrender.com/docs)

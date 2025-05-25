# API Empresas Chile 🇨🇱

![Deploy to Render](https://img.shields.io/badge/render-live-brightgreen?logo=render&style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-🚀-green?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql&style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)
[![UptimeRobot](https://img.shields.io/uptimerobot/status/m789123456-abcdef1234567890abcdef)](https://uptimerobot.com/)

---

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

## 🌐 API en línea

Esta API está desplegada en Render y disponible públicamente en:

🔗 https://api-empresas-chile.onrender.com  
📘 Documentación Swagger: [https://api-empresas-chile.onrender.com/docs](https://api-empresas-chile.onrender.com/docs)

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

## 📊 Ejemplo de uso del endpoint de estadísticas

Puedes consultar estadísticas agregadas de empresas con:

```http
GET /estadisticas
```

También puedes filtrar por año específico:

```http
GET /estadisticas?anio=2015
```

Esto devolverá un JSON con:

- Empresas creadas ese año (`por_anio`)
- Empresas por comuna (`por_comuna`)
- Empresas por rango de capital (`por_rango_capital`)

## 🗂️ Estructura del proyecto

```
.
├── app/               # Código principal de la API (modelos, rutas, etc.)
├── scripts/           # Scripts de carga desde CSV
├── data/              # CSV con datos del RES (no se sube)
├── .env.example       # Variables de entorno
├── requirements.txt   # Dependencias
├── LICENSE            # Licencia MIT
└── README.md          # Esta documentación
```

## 📦 Dependencias clave

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [psycopg2](https://pypi.org/project/psycopg2/)
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/)

## 📝 Licencia

Este proyecto está licenciado bajo los términos de la [Licencia MIT](LICENSE).

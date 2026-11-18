# api-madi-platform-dev
api-madi-platform-dev repo


Backend REST para Fundación MADI, utilizando Python 3.14, FastAPI, PostgreSQL, SQLAlchemy, Pydantic y Alembic.

backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── health.py
│   │           └── diseases.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   └── disease.py
│   │
│   └── schemas/
│       └── disease.py
│
├── tests/
│   ├── test_health.py
│   └── test_diseases.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
└── docker-compose.yml

pip install -r requirements.txt
fastapi: framework para construir la API.
uvicorn: servidor que ejecuta la aplicación ASGI.
sqlalchemy: ORM para trabajar con tablas y registros.
psycopg: driver de PostgreSQL.
alembic: versionamiento de esquemas de base de datos.
pydantic: validación de información.
pydantic-settings: configuración desde variables de entorno.
pytest: framework de testing.
httpx: cliente HTTP para probar endpoints.

dotenv:
APP_NAME=Fundacion MADI API
APP_VERSION=1.0.0
APP_ENV=development
DATABASE_URL=postgresql+psycopg://madi_user:madi_dev_password@localhost:5432/madi_db
API_V1_PREFIX=/api/v1

Archivo app/database/base.py
Aquí empieza la separación entre la lógica de negocio y la infraestructura de datos.
¿Qué hace?

Define la clase base de la cual heredarán todos los modelos SQLAlchemy.
Por ejemplo, nuestra entidad Disease heredará de Base.
Esto permite que SQLAlchemy identifique las tablas que forman parte del modelo de datos.

----------------------------------------------------------------------------------------
Archivo app/database/session.py
¿Qué hace?

Este archivo administra la conexión a PostgreSQL.

Conceptos importantes:
- create_engine: crea el motor de conexión.
- pool_pre_ping=True: verifica que una conexión del pool siga activa antes de utilizarla.
- sessionmaker: crea sesiones para ejecutar consultas.
- autoflush=False: evita sincronizaciones automáticas inesperadas antes de una consulta.
- expire_on_commit=False: permite acceder a los atributos de objetos después del commit.
No abriremos una conexión manual por cada endpoint. Utilizaremos sesiones administradas por SQLAlchemy.

----------------------------------------------------------------------------------------
Archivo app/api/deps.py
¿Qué hace?

Implementa una dependencia de FastAPI para administrar las sesiones de base de datos.

Cuando un endpoint necesita PostgreSQL:
1. FastAPI ejecuta get_db().
2. Se crea una sesión.
3. El endpoint utiliza la sesión.
4. Al finalizar la solicitud, se cierra la sesión.
Esto evita conexiones abiertas innecesariamente y facilita las pruebas automatizadas.

----------------------------------------------------------------------------------------

Archivo app/models/disease.py
¿Qué representa este modelo?

Es la representación de una tabla de PostgreSQL.
Tabla: diseases
Columna	Tipo	Descripción
id	INTEGER	Identificador
name	VARCHAR(150)	Nombre
slug	VARCHAR(180)	Identificador URL único
summary	VARCHAR(500)	Resumen
description	TEXT	Descripción detallada
is_published	BOOLEAN	Publicación
created_at	TIMESTAMPTZ	Fecha de creación
updated_at	TIMESTAMPTZ	Última actualización


Por ejemplo, podremos almacenar enfermedades como:
- Distrofia muscular de Duchenne.
- Distrofia muscular de Becker.
- Atrofia muscular espinal.
En este proyecto utilizaremos contenido educativo revisado por profesionales. No almacenaremos diagnósticos individuales en esta tabla.

Nota técnica: en una versión posterior mejoraremos el tratamiento de timestamps usando UTC explícito mediante una función de fecha consciente de zona horaria.

----------------------------------------------------------------------------------------
Archivo app/schemas/disease.py

¿Por qué necesitamos tres esquemas?
Esquema	Uso
DiseaseBase	Campos comunes
DiseaseCreate	Validar creación
DiseaseUpdate	Validar modificaciones parciales
DiseaseResponse	Definir la respuesta HTTP

----------------------------------------------------------------------------------------
Archivo app/api/v1/endpoints/health.py

Tenemos dos comprobaciones diferentes:
Endpoint	Función
/health/live	Comprueba que el proceso API responde
/health/ready	Comprueba que API y PostgreSQL están disponibles

Esta distinción es importante en Kubernetes y también resulta útil para configurar los health checks de Azure App Service.

----------------------------------------------------------------------------------------
Archivo app/api/v1/endpoints/diseases.py

Aquí implementaremos nuestro CRUD completo.

CRUD significa:
- Create: crear.
- Read: consultar.
- Update: actualizar.
- Delete: eliminar.

----------------------------------------------------------------------------------------
Archivo app/api/v1/router.py

Este archivo agrupa los diferentes módulos de la API.

Cuando agreguemos users, articles y events, los registraremos aquí.
----------------------------------------------------------------------------------------
Archivo app/main.py
Este será el punto de entrada principal de nuestra aplicación.
La responsabilidad de main.py debe ser inicializar la aplicación y registrar sus componentes.

No debe contener toda la lógica de negocio.

----------------------------------------------------------------------------------------
No queremos eliminar la base de datos y volver a crearla cada vez que modificamos un modelo.

Para eso utilizamos Alembic.

alembic init migrations
alembic revision --autogenerate -m "create diseases table"
alembic upgrade head
pytest -v

backend/
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
└── alembic.ini


# CV Generator API

Una API RESTful construida con FastAPI para generar y gestionar CV en formatos HTML y PDF.

## Características

- CRUD completo para perfiles de CV
- Generación de CV en formato HTML
- Exportación de CV a PDF
- Validación de datos con Pydantic
- Almacenamiento en MongoDB Atlas
- Documentación automática con Swagger/OpenAPI

## Requisitos

```bash
Python 3.10+
MongoDB Atlas cuenta y cluster
```

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd FastAPI
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
Crear un archivo `.env` con:
```env
MONGODB_URL=tu_url_de_mongodb_atlas
APP_NAME=CV Generator
APP_VERSION=1.0.0
DEBUG=True
```

## Estructura del Proyecto

```
FastAPI/
│
├── app.py                 # Punto de entrada de la aplicación
├── requirements.txt       # Dependencias del proyecto
│
├── routes/
│   └── user_routes.py    # Rutas para el manejo de perfiles
│
├── models/
│   └── user_models.py    # Modelos Pydantic para validación
│
├── db/
│   └── database.py       # Configuración y operaciones de MongoDB
│
├── templates/
│   └── cv_template.html  # Plantilla HTML para el CV
│
└── static/               # Archivos estáticos (CSS, JS, etc.)
```

## Endpoints API

### Perfiles

- `POST /api/v1/profiles` - Crear nuevo perfil
- `GET /api/v1/profiles` - Obtener todos los perfiles
- `GET /api/v1/profiles/{profile_id}` - Obtener perfil específico
- `PUT /api/v1/profiles/{profile_id}` - Actualizar perfil
- `DELETE /api/v1/profiles/{profile_id}` - Eliminar perfil

### Visualización y Descarga

- `GET /api/v1/profiles/{profile_id}/view` - Ver CV en HTML
- `GET /api/v1/profiles/{profile_id}/download` - Descargar CV en PDF

## Documentación API

La documentación interactiva está disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Ejecución

```bash
uvicorn app:app --reload
```

## Ejemplo de Uso

```python
# Crear un nuevo perfil
curl -X POST "http://localhost:8000/api/v1/profiles" -H "Content-Type: application/json" -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "+573001234567",
    "location": "Bogotá, Colombia",
    "summary": "Desarrollador Full Stack con experiencia...",
    "experiences": [...],
    "education": [...],
    "skills": [...],
    "languages": [...]
}'
```

## Tecnologías Utilizadas

- FastAPI
- MongoDB Atlas
- Pydantic
- Jinja2
- FPDF
- Python-dotenv

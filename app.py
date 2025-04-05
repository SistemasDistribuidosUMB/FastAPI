"""
CV Generator API - Aplicación Principal

Este módulo es el punto de entrada principal de la aplicación FastAPI para generar y gestionar CVs.
Configura la aplicación FastAPI, el sistema de logging, y los middlewares necesarios.
"""

import logging
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del sistema de logging
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG", "False").lower() == "true" else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger.info(f"Directorio base: {BASE_DIR}")

# Crear la aplicación FastAPI
app = FastAPI(
    title=os.getenv("APP_NAME", "CV Generator API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="API para generar CVs en formato PDF y HTML",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
static_path = os.path.join(BASE_DIR, "static")
logger.info(f"Directorio de archivos estáticos: {static_path}")
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Configurar templates
templates_path = os.path.join(BASE_DIR, "templates")
logger.info(f"Directorio de templates: {templates_path}")
templates = Jinja2Templates(directory=templates_path)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request path: {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Importar y registrar las rutas
from routes.user_routes import router
app.include_router(router)
logger.info("Rutas registradas:")
for route in app.routes:
    if hasattr(route, 'methods'):
        logger.info(f"  {route.path} [{route.methods}]")

# Manejador de errores global
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Manejador global de excepciones HTTP.
    Registra los errores en el log y devuelve una respuesta JSON apropiada.
    """
    logger.error(f"Error HTTP {exc.status_code}: {exc.detail}")
    return {
        "error": True,
        "status_code": exc.status_code,
        "message": exc.detail
    }

# Punto de entrada para ejecución directa
if __name__ == "__main__":
    import uvicorn
    # Ejecutar el servidor con recarga automática en desarrollo
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

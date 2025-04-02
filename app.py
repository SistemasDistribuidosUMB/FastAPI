# Este archivo es el punto de entrada principal de la aplicación FastAPI
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger.info(f"Directorio base: {BASE_DIR}")

# Crear la aplicación FastAPI
app = FastAPI(
    title="CV Generator API",
    description="API para generar CVs en formato PDF y HTML",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar archivos estáticos
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

# Si se ejecuta directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

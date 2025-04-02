# Este es el archivo principal que inicia la aplicación FastAPI
# Importamos las dependencias necesarias
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
import routes.user_routes

# FastAPI App

# Definimos la ruta principal de la aplicación
@app.get("/")
def read_root():
    """
    Ruta principal que muestra un mensaje de bienvenida
    Returns:
        dict: Un diccionario con el mensaje de bienvenida
    """
    return {"message": "Bienvenidos a FastAPI De la hoja de vida"}
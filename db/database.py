"""
Módulo de configuración y operaciones de base de datos MongoDB.

Este módulo maneja la conexión a MongoDB Atlas y proporciona funciones
para realizar operaciones CRUD (Create, Read, Update, Delete) en los perfiles de CV.
"""

import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Configuración del logger
logger = logging.getLogger(__name__)

# Obtener la URL de conexión de MongoDB desde las variables de entorno
MONGODB_URL = os.getenv("MONGODB_URL")
if not MONGODB_URL:
    raise ValueError("La URL de MongoDB no está configurada en las variables de entorno")

try:
    # Crear cliente de MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    # Seleccionar base de datos y colección
    db = client.cv_database
    profiles_collection = db.profiles
    
    logger.info("Conexión exitosa a MongoDB Atlas")
except Exception as e:
    logger.error(f"Error al conectar a MongoDB: {str(e)}")
    raise

async def create_profile_db(profile_data: dict) -> str:
    """
    Crea un nuevo perfil en la base de datos.

    Args:
        profile_data (dict): Datos del perfil a crear

    Returns:
        str: ID del perfil creado

    Raises:
        Exception: Si hay un error al crear el perfil
    """
    try:
        result = await profiles_collection.insert_one(profile_data)
        logger.info(f"Perfil creado con ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error al crear perfil: {str(e)}")
        raise

async def get_profile_by_id(profile_id: str) -> dict:
    """
    Obtiene un perfil específico por su ID.

    Args:
        profile_id (str): ID del perfil a buscar

    Returns:
        dict: Datos del perfil encontrado o None si no existe
    """
    try:
        profile = await profiles_collection.find_one({"_id": ObjectId(profile_id)})
        if profile:
            profile["_id"] = str(profile["_id"])
        return profile
    except Exception as e:
        logger.error(f"Error al obtener perfil {profile_id}: {str(e)}")
        return None

async def get_all_profiles() -> list:
    """
    Obtiene todos los perfiles almacenados.

    Returns:
        list: Lista de perfiles encontrados
    """
    try:
        profiles = []
        cursor = profiles_collection.find({})
        async for profile in cursor:
            profile["_id"] = str(profile["_id"])
            profiles.append(profile)
        return profiles
    except Exception as e:
        logger.error(f"Error al obtener perfiles: {str(e)}")
        return []

async def update_profile_db(profile_id: str, profile_data: dict) -> bool:
    """
    Actualiza un perfil existente.

    Args:
        profile_id (str): ID del perfil a actualizar
        profile_data (dict): Nuevos datos del perfil

    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    try:
        profile_data["updated_at"] = datetime.now()
        result = await profiles_collection.update_one(
            {"_id": ObjectId(profile_id)},
            {"$set": profile_data}
        )
        success = result.modified_count > 0
        if success:
            logger.info(f"Perfil {profile_id} actualizado exitosamente")
        else:
            logger.warning(f"No se encontró el perfil {profile_id} para actualizar")
        return success
    except Exception as e:
        logger.error(f"Error al actualizar perfil {profile_id}: {str(e)}")
        return False

async def delete_profile_db(profile_id: str) -> bool:
    """
    Elimina un perfil de la base de datos.

    Args:
        profile_id (str): ID del perfil a eliminar

    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario
    """
    try:
        result = await profiles_collection.delete_one({"_id": ObjectId(profile_id)})
        success = result.deleted_count > 0
        if success:
            logger.info(f"Perfil {profile_id} eliminado exitosamente")
        else:
            logger.warning(f"No se encontró el perfil {profile_id} para eliminar")
        return success
    except Exception as e:
        logger.error(f"Error al eliminar perfil {profile_id}: {str(e)}")
        return False
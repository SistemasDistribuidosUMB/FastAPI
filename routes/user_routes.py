"""
Rutas de la API para la gestión de perfiles de CV.

Este módulo contiene todas las rutas relacionadas con el manejo de perfiles
y la generación de CVs en diferentes formatos (HTML y PDF).
"""

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from models.user_models import Profile, ProfileUpdate
from typing import List
from uuid import uuid4
import os
import logging
from fpdf import FPDF
from datetime import datetime

# Configuración del sistema de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtenemos la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Importamos las dependencias necesarias de la base de datos
from db.database import (
    get_all_profiles,
    get_profile_by_id,
    create_profile_db,
    update_profile_db,
    delete_profile_db
)

# Configuramos el sistema de templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Creamos el router con la configuración de la API
router = APIRouter(
    prefix="/api/v1",
    tags=["CV Management"],
    responses={404: {"description": "Recurso no encontrado"}}
)

@router.post("/profiles", 
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo perfil",
    description="Crea un nuevo perfil de CV en la base de datos")
async def create_profile(profile: Profile):
    """
    Crea un nuevo perfil de CV.

    Args:
        profile (Profile): Datos del perfil a crear

    Returns:
        dict: ID del perfil creado y mensaje de éxito

    Raises:
        HTTPException: Si hay un error al crear el perfil
    """
    try:
        profile_dict = profile.dict()
        profile_id = await create_profile_db(profile_dict)
        return {"id": profile_id, "message": "Perfil creado exitosamente"}
    except Exception as e:
        logger.error(f"Error al crear perfil: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el perfil"
        )

@router.get("/profiles", 
    response_model=List[Profile],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los perfiles",
    description="Retorna una lista de todos los perfiles almacenados")
async def get_profiles():
    """
    Obtiene todos los perfiles de CV.

    Returns:
        List[Profile]: Lista de perfiles encontrados
    """
    return await get_all_profiles()

@router.get("/profiles/{profile_id}", 
    response_model=Profile,
    summary="Obtener un perfil específico",
    description="Obtiene un perfil específico por su ID")
async def get_profile(profile_id: str):
    """
    Obtiene un perfil específico por su ID.

    Args:
        profile_id (str): ID del perfil a buscar

    Returns:
        Profile: Datos del perfil encontrado

    Raises:
        HTTPException: Si el perfil no existe
    """
    profile = await get_profile_by_id(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado"
        )
    return profile

@router.put("/profiles/{profile_id}",
    response_model=dict,
    summary="Actualizar un perfil",
    description="Actualiza un perfil existente por su ID")
async def update_profile(profile_id: str, profile_update: ProfileUpdate):
    """
    Actualiza un perfil existente.

    Args:
        profile_id (str): ID del perfil a actualizar
        profile_update (ProfileUpdate): Datos a actualizar

    Returns:
        dict: Mensaje de éxito

    Raises:
        HTTPException: Si el perfil no existe o hay un error
    """
    profile_data = profile_update.dict(exclude_unset=True)
    if not profile_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay datos para actualizar"
        )
    
    success = await update_profile_db(profile_id, profile_data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado"
        )
    
    return {"message": "Perfil actualizado exitosamente"}

@router.delete("/profiles/{profile_id}",
    response_model=dict,
    summary="Eliminar un perfil",
    description="Elimina un perfil existente por su ID")
async def delete_profile(profile_id: str):
    """
    Elimina un perfil existente.

    Args:
        profile_id (str): ID del perfil a eliminar

    Returns:
        dict: Mensaje de éxito

    Raises:
        HTTPException: Si el perfil no existe
    """
    success = await delete_profile_db(profile_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado"
        )
    return {"message": "Perfil eliminado exitosamente"}

@router.get("/profiles/{profile_id}/view", 
    response_class=HTMLResponse,
    summary="Ver CV en formato HTML",
    description="Genera una vista HTML del CV")
async def view_cv(request: Request, profile_id: str):
    """
    Genera una vista HTML del CV.

    Args:
        request (Request): Objeto de solicitud FastAPI
        profile_id (str): ID del perfil a visualizar

    Returns:
        HTMLResponse: Página HTML con el CV

    Raises:
        HTTPException: Si el perfil no existe
    """
    profile = await get_profile_by_id(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado"
        )
    
    # Formatear experiencias
    experiences_html = ""
    for exp in profile["experiences"]:
        experiences_html += f"""
        <div class="mb-4">
            <h4>{exp["position"]} - {exp["company"]}</h4>
            <p class="text-muted">{exp["start_date"]} - {exp["end_date"]}</p>
            <p>{exp["description"]}</p>
        </div>
        """
    
    # Formatear educación
    education_html = ""
    for edu in profile["education"]:
        education_html += f"""
        <div class="mb-4">
            <h4>{edu["degree"]} en {edu["field"]}</h4>
            <h5>{edu["institution"]}</h5>
            <p class="text-muted">{edu["start_date"]} - {edu["end_date"]}</p>
        </div>
        """
    
    # Formatear habilidades y lenguajes
    skills_html = ", ".join([f"{skill['name']} ({skill['level']})" for skill in profile["skills"]])
    languages_html = ", ".join([f"{lang['name']} ({lang['level']})" for lang in profile["languages"]])
    
    return templates.TemplateResponse(
        "cv_template.html",
        {
            "request": request,
            "name": profile["name"],
            "email": profile["email"],
            "phone": profile["phone"],
            "location": profile["location"],
            "summary": profile["summary"],
            "experiences": experiences_html,
            "education": education_html,
            "skills": skills_html,
            "languages": languages_html
        }
    )

@router.get("/profiles/{profile_id}/download",
    response_class=FileResponse,
    summary="Descargar CV en PDF",
    description="Genera y descarga el CV en formato PDF")
async def generate_cv(profile_id: str):
    """
    Genera y descarga el CV en formato PDF.

    Args:
        profile_id (str): ID del perfil a descargar

    Returns:
        FileResponse: Archivo PDF del CV

    Raises:
        HTTPException: Si el perfil no existe o hay un error
    """
    profile = await get_profile_by_id(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado"
        )
    
    try:
        # Crear PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Configurar fuentes
        pdf.set_font("Arial", "B", 16)
        
        # Encabezado
        pdf.cell(0, 10, profile["name"], ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Email: {profile['email']}", ln=True)
        pdf.cell(0, 10, f"Teléfono: {profile['phone']}", ln=True)
        pdf.cell(0, 10, f"Ubicación: {profile['location']}", ln=True)
        
        # Resumen
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Resumen Profesional", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, profile["summary"])
        
        # Experiencia
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Experiencia Laboral", ln=True)
        for exp in profile["experiences"]:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"{exp['position']} - {exp['company']}", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"{exp['start_date']} - {exp['end_date']}", ln=True)
            pdf.multi_cell(0, 10, exp["description"])
            pdf.ln(5)
        
        # Guardar PDF
        pdf_path = os.path.join(BASE_DIR, "temp", f"cv_{profile_id}.pdf")
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        pdf.output(pdf_path)
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"cv_{profile['name'].replace(' ', '_')}.pdf"
        )
    except Exception as e:
        logger.error(f"Error al generar PDF: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al generar el PDF"
        )

# Incluir las rutas en la aplicación principal
from app import app
app.include_router(router)

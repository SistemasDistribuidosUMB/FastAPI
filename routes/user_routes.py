# Este archivo contiene todas las rutas relacionadas con el manejo de perfiles y generación de CVs
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from models.user_models import Profile
from uuid import uuid4
import os
import logging
from fpdf import FPDF
from fastapi.staticfiles import StaticFiles

# Configuración del sistema de logging para debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtenemos la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Importamos las dependencias necesarias
from db.database import database

# Configuramos el sistema de templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Creamos el router con la configuración de la API
router = APIRouter(
    prefix="",  # Sin prefijo para mantener las URLs limpias
    tags=["CV Management"],  # Tag para agrupar en la documentación
    responses={404: {"description": "Recurso no encontrado"}}  # Respuesta por defecto para 404
)

@router.post("/profile", 
    response_model=dict,
    summary="Crear un nuevo perfil",
    description="Crea un nuevo perfil de usuario en la base de datos")
async def create_profile(profile: Profile):
    """
    Crea un nuevo perfil de usuario con la siguiente información:
    
    - **name**: Nombre completo del usuario
    - **email**: Correo electrónico de contacto
    - **phone**: Número de teléfono
    - **location**: Ubicación/Ciudad
    - **experiences**: Lista de experiencias laborales
    - **education**: Lista de estudios realizados
    - **skills**: Lista de habilidades técnicas
    - **languages**: Lista de idiomas que domina
    
    Retorna el ID único del perfil creado.
    """
    try:
        # Generamos un ID único para el perfil
        user_id = str(uuid4())
        
        # Convertimos el modelo Pydantic a diccionario
        profile_dict = profile.model_dump()
        profile_dict["user_id"] = user_id
        
        # Guardamos en la base de datos
        database.get_collection("profiles").insert_one(profile_dict)
        
        return {"message": "Perfil creado exitosamente", "user_id": user_id}
    except Exception as e:
        logger.error(f"Error al crear perfil: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear el perfil")

@router.get("/profile/{user_id}", 
    response_model=Profile,
    summary="Obtener un perfil",
    description="Obtiene los datos de un perfil específico")
async def get_profile(user_id: str):
    """
    Obtiene los datos completos de un perfil por su ID
    
    - **user_id**: ID único del perfil a buscar
    
    Retorna todos los datos del perfil si existe.
    """
    try:
        # Buscamos el perfil en la base de datos
        profile = database.get_collection("profiles").find_one(
            {"user_id": user_id},
            {"_id": 0}  # Excluimos el _id de MongoDB
        )
        
        if not profile:
            raise HTTPException(status_code=404, detail="Perfil no encontrado")
            
        return profile
    except Exception as e:
        logger.error(f"Error al obtener perfil: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener el perfil")

@router.get("/view-cv/{user_id}", response_class=HTMLResponse)
async def view_cv(request: Request, user_id: str):
    """
    Genera una vista HTML del CV
    """
    try:
        logger.info(f"Buscando perfil con ID: {user_id}")
        profile = database.get_collection("profiles").find_one({"user_id": user_id}, {"_id": 0})
        
        if not profile:
            logger.error(f"Perfil no encontrado para ID: {user_id}")
            raise HTTPException(status_code=404, detail="Perfil no encontrado")

        logger.info(f"Perfil encontrado: {profile}")
        
        # Formatear experiencias
        experiences = ""
        for exp in profile.get("experiences", []):
            experiences += f"""
            <div class="experience-item mb-4">
                <h4>{exp['title']}</h4>
                <h5>{exp['company']}</h5>
                <p class="text-muted">{exp['start_date']} - {exp.get('end_date', 'Presente')}</p>
                <p>{exp['description']}</p>
            </div>
            """

        # Formatear educación
        education = ""
        for edu in profile.get("education", []):
            education += f"""
            <div class="education-item mb-4">
                <h4>{edu['degree']}</h4>
                <h5>{edu['institution']}</h5>
                <p class="text-muted">{edu['year']}</p>
            </div>
            """

        logger.info("Renderizando template")
        return templates.TemplateResponse(
            "cv_template.html",
            {
                "request": request,
                "name": profile.get("name", ""),
                "email": profile.get("email", ""),
                "phone": profile.get("phone", ""),
                "location": profile.get("location", ""),
                "experiences": experiences,
                "education": education,
                "skills": ", ".join(profile.get("skills", [])),
                "languages": ", ".join(profile.get("languages", [])),
                "user_id": user_id
            }
        )
    except Exception as e:
        logger.error(f"Error al generar CV HTML: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/generate-cv/{user_id}", 
    response_class=FileResponse,
    summary="Generar CV en PDF",
    description="Genera una versión PDF del CV para descargar")
async def generate_cv(user_id: str):
    """
    Genera una versión PDF del CV para descargar
    
    - **user_id**: ID único del perfil a generar en PDF
    
    Retorna un archivo PDF descargable.
    """
    try:
        # Buscamos el perfil en la base de datos
        profile = database.get_collection("profiles").find_one(
            {"user_id": user_id},
            {"_id": 0}
        )
        
        if not profile:
            raise HTTPException(status_code=404, detail="Perfil no encontrado")

        # Creamos el PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Información personal
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, profile.get("name", ""), ln=True, align='C')
        pdf.set_font('Arial', '', 12)
        contact_info = f"{profile.get('email', '')} | {profile.get('phone', '')} | {profile.get('location', '')}"
        pdf.cell(0, 10, contact_info, ln=True, align='C')
        
        # Experiencia
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Experiencia', ln=True)
        pdf.set_font('Arial', '', 12)
        for exp in profile.get("experiences", []):
            pdf.cell(0, 10, f"{exp['title']} - {exp['company']}", ln=True)
            pdf.cell(0, 10, f"{exp['start_date']} - {exp.get('end_date', 'Presente')}", ln=True)
            pdf.multi_cell(0, 10, exp['description'])
            pdf.ln(5)
        
        # Educación
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Educación', ln=True)
        pdf.set_font('Arial', '', 12)
        for edu in profile.get("education", []):
            pdf.cell(0, 10, f"{edu['degree']} - {edu['institution']}", ln=True)
            pdf.cell(0, 10, edu['year'], ln=True)
            pdf.ln(5)
        
        # Habilidades
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Habilidades', ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, ", ".join(profile.get("skills", [])))
        
        # Idiomas
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Idiomas', ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, ", ".join(profile.get("languages", [])))
        
        # Guardamos el PDF
        pdf_path = os.path.join(BASE_DIR, "temp")
        os.makedirs(pdf_path, exist_ok=True)
        pdf_file = os.path.join(pdf_path, f"cv_{user_id}.pdf")
        pdf.output(pdf_file)
        
        return FileResponse(
            pdf_file,
            media_type="application/pdf",
            filename=f"cv_{profile.get('name', 'cv').replace(' ', '_')}.pdf"
        )
        
    except Exception as e:
        logger.error(f"Error al generar PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Incluir las rutas en la aplicación principal
from app import app
app.include_router(router)

"""
Modelos de datos para la aplicación CV Generator.

Este módulo define los modelos Pydantic utilizados para la validación de datos
y la serialización/deserialización de los perfiles de CV.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class Experience(BaseModel):
    """
    Modelo para la experiencia laboral.
    
    Attributes:
        company (str): Nombre de la empresa
        position (str): Cargo ocupado
        start_date (str): Fecha de inicio (formato: YYYY-MM)
        end_date (str): Fecha de finalización (formato: YYYY-MM)
        description (str): Descripción de responsabilidades y logros
    """
    company: str = Field(..., min_length=2, max_length=100)
    position: str = Field(..., min_length=2, max_length=100)
    start_date: str = Field(..., pattern="^\\d{4}-\\d{2}$")
    end_date: str = Field(..., pattern="^\\d{4}-\\d{2}$")
    description: str = Field(..., min_length=10, max_length=500)

class Education(BaseModel):
    """
    Modelo para la formación académica.
    
    Attributes:
        institution (str): Nombre de la institución educativa
        degree (str): Título obtenido
        field (str): Campo de estudio
        start_date (str): Fecha de inicio (formato: YYYY-MM)
        end_date (str): Fecha de finalización (formato: YYYY-MM)
    """
    institution: str = Field(..., min_length=2, max_length=100)
    degree: str = Field(..., min_length=2, max_length=100)
    field: str = Field(..., min_length=2, max_length=100)
    start_date: str = Field(..., pattern="^\\d{4}-\\d{2}$")
    end_date: str = Field(..., pattern="^\\d{4}-\\d{2}$")

class Skill(BaseModel):
    """
    Modelo para habilidades técnicas o blandas.
    
    Attributes:
        name (str): Nombre de la habilidad
        level (str): Nivel de competencia
    """
    name: str = Field(..., min_length=2, max_length=50)
    level: str = Field(..., min_length=2, max_length=50)

class Language(BaseModel):
    """
    Modelo para idiomas.
    
    Attributes:
        name (str): Nombre del idioma
        level (str): Nivel de competencia (e.g., A1, B2, C1)
    """
    name: str = Field(..., min_length=2, max_length=50)
    level: str = Field(..., pattern="^[A-C][1-2]$")

class Profile(BaseModel):
    """
    Modelo principal para el perfil completo del CV.
    
    Attributes:
        name (str): Nombre completo
        email (EmailStr): Correo electrónico
        phone (str): Número de teléfono
        location (str): Ubicación
        summary (str): Resumen profesional
        experiences (List[Experience]): Lista de experiencias laborales
        education (List[Education]): Lista de formación académica
        skills (List[Skill]): Lista de habilidades
        languages (List[Language]): Lista de idiomas
        created_at (datetime): Fecha de creación
        updated_at (datetime): Fecha de última actualización
    """
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., pattern="^\\+?[0-9]{10,15}$")
    location: str = Field(..., min_length=2, max_length=100)
    summary: str = Field(..., min_length=50, max_length=500)
    experiences: List[Experience]
    education: List[Education]
    skills: List[Skill]
    languages: List[Language]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class ProfileUpdate(BaseModel):
    """
    Modelo para actualización parcial del perfil.
    Todos los campos son opcionales.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern="^\\+?[0-9]{10,15}$")
    location: Optional[str] = Field(None, min_length=2, max_length=100)
    summary: Optional[str] = Field(None, min_length=50, max_length=500)
    experiences: Optional[List[Experience]] = None
    education: Optional[List[Education]] = None
    skills: Optional[List[Skill]] = None
    languages: Optional[List[Language]] = None

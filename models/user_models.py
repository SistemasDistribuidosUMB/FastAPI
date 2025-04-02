# Este archivo define los modelos de datos usando Pydantic para validación
from pydantic import BaseModel
from typing import List, Optional

class Experience(BaseModel):
    """
    Modelo para representar la experiencia laboral
    Attributes:
        title (str): Título o cargo del trabajo
        company (str): Nombre de la empresa
        start_date (str): Fecha de inicio
        end_date (Optional[str]): Fecha de finalización (opcional)
        description (str): Descripción de las responsabilidades y logros
    """
    title: str
    company: str
    start_date: str
    end_date: Optional[str] = None
    description: str

class Education(BaseModel):
    """
    Modelo para representar la educación
    Attributes:
        degree (str): Título o grado obtenido
        institution (str): Nombre de la institución educativa
        year (str): Año de graduación
    """
    degree: str
    institution: str
    year: str

class Profile(BaseModel):
    """
    Modelo principal para el perfil del CV
    Attributes:
        name (str): Nombre completo
        email (str): Correo electrónico
        phone (str): Número de teléfono
        location (str): Ubicación o ciudad
        experiences (List[Experience]): Lista de experiencias laborales
        education (List[Education]): Lista de estudios realizados
        skills (List[str]): Lista de habilidades
        languages (List[str]): Lista de idiomas
    """
    name: str
    email: str
    phone: str
    location: str
    experiences: List[Experience]
    education: List[Education]
    skills: List[str]
    languages: List[str]

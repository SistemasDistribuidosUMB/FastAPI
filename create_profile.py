# Script para crear un perfil de ejemplo usando la API
import requests
import json

# Datos de ejemplo para el perfil
profile_data = {
    "name": "Santiago Ángel",
    "email": "santiago.angel@example.com",
    "phone": "+57 300 123 4567",
    "location": "Bogotá, Colombia",
    "experiences": [
        {
            "title": "Desarrollador Full Stack",
            "company": "Tech Solutions",
            "start_date": "2023-01",
            "end_date": "2024-12",
            "description": "Desarrollo de aplicaciones web usando Python, FastAPI y React"
        }
    ],
    "education": [
        {
            "institution": "Universidad Nacional",
            "degree": "Ingeniería de Sistemas",
            "year": "2025"
        }
    ],
    "skills": ["Python", "FastAPI", "MongoDB", "React", "Docker"],
    "languages": ["Español", "Inglés"]
}

# Enviar solicitud POST para crear el perfil
response = requests.post(
    'http://127.0.0.1:8000/profile',
    json=profile_data
)

# Imprimir la respuesta
print(response.json())

import requests
import json

url = "http://localhost:8000/api/v1/profiles"
headers = {"Content-Type": "application/json"}

data = {
    "name": "Santiago Angel",
    "email": "santiago@example.com",
    "phone": "+573001234567",
    "location": "Bogotá, Colombia",
    "summary": "Desarrollador Full Stack con experiencia en Python y FastAPI.",
    "experiences": [
        {
            "company": "Tech Solutions",
            "position": "Desarrollador Full Stack",
            "start_date": "2023-01",
            "end_date": "2024-03",
            "description": "Desarrollo de aplicaciones web usando FastAPI."
        }
    ],
    "education": [
        {
            "institution": "Universidad Nacional",
            "degree": "Ingeniería de Sistemas",
            "field": "Computación",
            "start_date": "2020-01",
            "end_date": "2024-12"
        }
    ],
    "skills": [
        {
            "name": "Python",
            "level": "Avanzado"
        }
    ],
    "languages": [
        {
            "name": "Español",
            "level": "C2"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

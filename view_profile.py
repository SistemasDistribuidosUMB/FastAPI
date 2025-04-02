# Script para visualizar un perfil existente en formato legible
import requests
import json

# ID del perfil a visualizar
user_id = "250b0895-0aa7-44d3-8eab-e29605d8ed40"

# Obtener el perfil de la API
response = requests.get(f"http://127.0.0.1:8000/profile/{user_id}")
profile = response.json()

# Mostrar la información del perfil de manera formateada
print("\n=== PERFIL CV ===")
print(f"\nNombre: {profile['name']}")
print(f"Email: {profile['email']}")
print(f"Teléfono: {profile['phone']}")
print(f"Ubicación: {profile['location']}")

print("\n=== EXPERIENCIA ===")
for exp in profile['experiences']:
    print(f"\n• {exp['title']} en {exp['company']}")
    print(f"  {exp['start_date']} - {exp.get('end_date', 'Actual')}")
    print(f"  {exp['description']}")

print("\n=== EDUCACIÓN ===")
for edu in profile['education']:
    print(f"\n• {edu['degree']}")
    print(f"  {edu['institution']} ({edu['year']})")

print("\n=== HABILIDADES ===")
print(", ".join(profile['skills']))

print("\n=== IDIOMAS ===")
print(", ".join(profile['languages']))
print()

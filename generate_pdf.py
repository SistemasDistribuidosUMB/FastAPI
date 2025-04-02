# Script para generar y descargar el CV en formato PDF
import requests
import os
import time

def download_pdf(user_id, max_retries=3):
    """
    Intenta descargar el PDF del CV con reintentos en caso de error
    Args:
        user_id (str): ID del perfil para generar el CV
        max_retries (int): Número máximo de intentos de descarga
    Returns:
        bool: True si la descarga fue exitosa, False en caso contrario
    """
    for attempt in range(max_retries):
        try:
            # Realizar la petición al endpoint de generación de PDF
            response = requests.get(
                f"http://127.0.0.1:8000/generate-cv/{user_id}",
                stream=True
            )
            
            if response.status_code == 200:
                # Guardar el PDF en el disco
                filename = f"cv_{user_id}.pdf"
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"\nPDF generado exitosamente: {os.path.abspath(filename)}")
                return True
            else:
                print(f"\nError al generar el PDF: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"\nIntento {attempt + 1} fallido. Reintentando en 2 segundos...")
                time.sleep(2)
            else:
                print(f"\nError después de {max_retries} intentos: {str(e)}")
                return False

if __name__ == "__main__":
    # ID del perfil para el cual queremos generar el CV
    user_id = "250b0895-0aa7-44d3-8eab-e29605d8ed40"
    download_pdf(user_id)

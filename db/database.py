# Este archivo maneja la conexión y operaciones con la base de datos MongoDB
from pymongo import MongoClient

class Database:
    """
    Clase para manejar la conexión y operaciones con MongoDB
    """
    def __init__(self):
        """
        Inicializa la conexión a MongoDB usando la URL de conexión
        La base de datos se llama 'cv_database'
        """
        # URL de conexión de MongoDB Compass
        self.client = MongoClient('mongodb+srv://santiagoangel5090:Ihvtdzw8@cluster0.haqs6.mongodb.net/', 
            tlsAllowInvalidCertificates=True  # Desactiva verificación de SSL
        )
        self.db = self.client["cv_database"]
    
    def get_collection(self, collection_name: str):
        """
        Obtiene una colección específica de la base de datos
        Args:
            collection_name (str): Nombre de la colección a obtener
        Returns:
            Collection: Objeto de colección de MongoDB
        """
        return self.db[collection_name]

# Crear una instancia global de la base de datos
database = Database()
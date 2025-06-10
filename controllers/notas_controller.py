# Controlador de Notas para Firebase
import logging
from config import FIREBASE_CREDENTIALS_JSON, FIREBASE_STORAGE_BUCKET
from controllers.firebase_controller import db
from typing import Dict, Any

async def agregar_nota(user_id: str, nota_data: Dict[str, Any]) -> None:
    """
    Agrega una nota a la colección 'notas' en Firebase
    
    Args:
        user_id: ID del usuario en Firebase
        nota_data: Diccionario con los datos de la nota
    """
    try:
        await db.collection('usuarios').document(str(user_id)).collection('notas').add(nota_data)
    except Exception as e:
        logging.error(f"Error al agregar nota: {e}")
        raise

async def obtener_notas(user_id: str) -> list:
    """
    Obtiene todas las notas de un usuario
    
    Args:
        user_id: ID del usuario en Firebase
        
    Returns:
        list: Lista de notas del usuario
    """
    try:
        notas_ref = db.collection('usuarios').document(str(user_id)).collection('notas')
        docs = await notas_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        logging.error(f"Error al obtener notas: {e}")
        return []

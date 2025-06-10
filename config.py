import os
import json
from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()

# Validación de configuraciones
if not os.getenv('TELEGRAM_TOKEN'):
    raise ValueError("Falta el token de Telegram en el archivo .env")
if not os.getenv('FIREBASE_CREDENTIALS_JSON'):
    raise ValueError("Falta la ruta de credenciales de Firebase en el archivo .env")
if not os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON'):
    raise ValueError("Falta la ruta de credenciales de Google Sheets en el archivo .env")
if not os.getenv('GOOGLE_SHEETS_ID'):
    raise ValueError("Falta el ID de la hoja de cálculo en el archivo .env")
if not os.getenv('GOOGLE_CALENDAR_ID'):
    raise ValueError("Falta el ID del calendario en el archivo .env")
if not os.getenv('GEMINI_API_KEY'):
    raise ValueError("Falta la API Key de Gemini en el archivo .env")
if not os.getenv('GEMINI_BASE_URL'):
    raise ValueError("Falta la URL base de Gemini en el archivo .env")

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FIREBASE_CREDENTIALS_JSON = os.getenv('FIREBASE_CREDENTIALS_JSON')
FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET')
GOOGLE_SHEETS_CREDENTIALS_JSON = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON')
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
GOOGLE_CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID')
GOOGLE_TASKS_ID = os.getenv('GOOGLE_TASKS_ID')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL')
GEMINI_BASE_URL = os.getenv('GEMINI_BASE_URL')

# Cargar las credenciales de Firebase desde un secreto
FIREBASE_CREDENTIALS_JSON = os.getenv('FIREBASE_CREDENTIALS_JSON')
if FIREBASE_CREDENTIALS_JSON:
    # Convertir el contenido del secreto en un diccionario
    firebase_credentials_dict = json.loads(FIREBASE_CREDENTIALS_JSON)
    cred = credentials.Certificate(firebase_credentials_dict)  # Modificación: Inicialización directa desde el JSON
else:
    raise ValueError("La variable de entorno FIREBASE_CREDENTIALS_JSON no está configurada.")  # Modificación: Validación de la variable de entorno

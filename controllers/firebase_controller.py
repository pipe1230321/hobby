# Controlador de Firebase (Firestore y Storage)
import os
import tempfile  # 🟢 Importamos tempfile para crear un archivo temporal con las credenciales
import firebase_admin
from firebase_admin import credentials, firestore, storage
from config import FIREBASE_CREDENTIALS_JSON, FIREBASE_STORAGE_BUCKET

# 🟢 MODIFICACIÓN: Crear un archivo temporal desde el contenido de la variable de entorno
# Esto es necesario en Render u otros entornos donde las credenciales están como string JSON
if FIREBASE_CREDENTIALS_JSON:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(FIREBASE_CREDENTIALS_JSON.encode())  # Escribimos el JSON como archivo
        temp_file_path = temp_file.name  # Obtenemos la ruta temporal

    cred = credentials.Certificate(temp_file_path)  # Cargamos credenciales desde archivo temporal
else:
    raise ValueError("La variable de entorno FIREBASE_CREDENTIALS_JSON no está configurada.")

# 🟢 MODIFICACIÓN: inicialización segura de Firebase App si no está inicializada aún
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'storageBucket': FIREBASE_STORAGE_BUCKET})

# Firestore y Storage listos para usarse
db = firestore.client()
bucket = storage.bucket()

# ---------------------------
# Usuarios
# ---------------------------

def guardar_usuario(user_id, datos):
    db.collection('usuarios').document(str(user_id)).set(datos, merge=True)

def obtener_usuario(user_id):
    return db.collection('usuarios').document(str(user_id)).get().to_dict()

# ---------------------------
# Ingresos y gastos
# ---------------------------

def registrar_movimiento(user_id, movimiento):
    db.collection('usuarios').document(str(user_id)).collection('movimientos').add(movimiento)

def obtener_movimientos(user_id):
    return [doc.to_dict() for doc in db.collection('usuarios').document(str(user_id)).collection('movimientos').stream()]

# ---------------------------
# Tareas y notas
# ---------------------------

def agregar_tarea(user_id, tarea):
    db.collection('usuarios').document(str(user_id)).collection('tareas').add(tarea)

def obtener_tareas(user_id):
    return [doc.to_dict() for doc in db.collection('usuarios').document(str(user_id)).collection('tareas').stream()]

# ---------------------------
# Archivos
# ---------------------------

def subir_archivo(nombre, archivo):
    blob = bucket.blob(nombre)
    blob.upload_from_file(archivo)
    return blob.public_url

def subir_archivo(user_id, file_path, nombre):
    blob = bucket.blob(f"{user_id}/{nombre}")
    blob.upload_from_filename(file_path)
    return blob.public_url

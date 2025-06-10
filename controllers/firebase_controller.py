# Controlador de Firebase (Firestore y Storage)
import firebase_admin
from firebase_admin import credentials, firestore, storage
from config import FIREBASE_CREDENTIALS_JSON, FIREBASE_STORAGE_BUCKET

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_JSON)
    firebase_admin.initialize_app(cred, {'storageBucket': FIREBASE_STORAGE_BUCKET})
db = firestore.client()
bucket = storage.bucket()

# Usuarios
def guardar_usuario(user_id, datos):
    db.collection('usuarios').document(str(user_id)).set(datos, merge=True)

def obtener_usuario(user_id):
    return db.collection('usuarios').document(str(user_id)).get().to_dict()

# Ingresos y gastos

def registrar_movimiento(user_id, movimiento):
    db.collection('usuarios').document(str(user_id)).collection('movimientos').add(movimiento)

def obtener_movimientos(user_id):
    return [doc.to_dict() for doc in db.collection('usuarios').document(str(user_id)).collection('movimientos').stream()]

# Tareas y notas

def agregar_tarea(user_id, tarea):
    db.collection('usuarios').document(str(user_id)).collection('tareas').add(tarea)

def obtener_tareas(user_id):
    return [doc.to_dict() for doc in db.collection('usuarios').document(str(user_id)).collection('tareas').stream()]

# Archivos

def subir_archivo(nombre, archivo):
    blob = bucket.blob(nombre)
    blob.upload_from_file(archivo)
    return blob.public_url

def subir_archivo(user_id, file_path, nombre):
    blob = bucket.blob(f"{user_id}/{nombre}")
    blob.upload_from_filename(file_path)
    return blob.public_url

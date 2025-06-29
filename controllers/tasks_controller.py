# Controlador de Google Tasks
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import json
from config import GOOGLE_SHEETS_CREDENTIALS_JSON, GOOGLE_TASKS_ID

SCOPES = ['https://www.googleapis.com/auth/tasks']

# Convertimos el JSON de la variable a dict
info = json.loads(GOOGLE_SHEETS_CREDENTIALS_JSON)
creds = Credentials.from_service_account_info(info, scopes=SCOPES)

service = build('tasks', 'v1', credentials=creds)

def crear_tarea(titulo):
    tarea = {'title': titulo}
    return service.tasks().insert(tasklist=GOOGLE_TASKS_ID, body=tarea).execute()

def listar_tareas():
    return service.tasks().list(tasklist=GOOGLE_TASKS_ID).execute().get('items', [])

def completar_tarea(task_id):
    return service.tasks().patch(tasklist=GOOGLE_TASKS_ID, task=task_id, body={'status': 'completed'}).execute()

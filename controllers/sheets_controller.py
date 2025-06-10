import os
import json
import gspread
from google.oauth2.service_account import Credentials

# Ámbitos para Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Obtener JSON de la variable de entorno
json_str = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON')

# Convertir el string JSON a diccionario Python
info = json.loads(json_str)

# Crear credenciales a partir del diccionario
creds = Credentials.from_service_account_info(info, scopes=SCOPES)

# Autorizar gspread con las credenciales
gc = gspread.authorize(creds)

# Abrir la hoja de cálculo por ID, que también debe estar en variable de entorno
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
sheet = gc.open_by_key(GOOGLE_SHEETS_ID)

def registrar_movimiento_sheet(fecha, categoria, monto, descripcion):
    ws = sheet.worksheet('Movimientos')
    ws.append_row([fecha, categoria, monto, descripcion])

def obtener_movimientos_sheet():
    ws = sheet.worksheet('Movimientos')
    return ws.get_all_records()

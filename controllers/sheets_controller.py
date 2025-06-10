# Controlador de Google Sheets
import gspread
import json
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEETS_CREDENTIALS_JSON, GOOGLE_SHEETS_ID

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Convertimos el contenido JSON en un diccionario Python
info = json.loads(GOOGLE_SHEETS_CREDENTIALS_JSON)

# Creamos las credenciales usando el diccionario de la cuenta de servicio
creds = Credentials.from_service_account_info(info, scopes=SCOPES)

# Autorizamos gspread con las credenciales creadas
gc = gspread.authorize(creds)

# Abrimos la hoja de cálculo por ID
sheet = gc.open_by_key(GOOGLE_SHEETS_ID)

def registrar_movimiento_sheet(fecha, categoria, monto, descripcion):
    ws = sheet.worksheet('Movimientos')
    ws.append_row([fecha, categoria, monto, descripcion])

def obtener_movimientos_sheet():
    ws = sheet.worksheet('Movimientos')
    return ws.get_all_records()

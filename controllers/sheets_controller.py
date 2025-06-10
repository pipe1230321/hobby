# Controlador de Google Sheets
import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEETS_CREDENTIALS_JSON, GOOGLE_SHEETS_ID

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file(GOOGLE_SHEETS_CREDENTIALS_JSON, scopes=SCOPES)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(GOOGLE_SHEETS_ID)

def registrar_movimiento_sheet(fecha, categoria, monto, descripcion):
    ws = sheet.worksheet('Movimientos')
    ws.append_row([fecha, categoria, monto, descripcion])

def obtener_movimientos_sheet():
    ws = sheet.worksheet('Movimientos')
    return ws.get_all_records()

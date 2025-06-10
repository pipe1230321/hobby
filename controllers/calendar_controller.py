# Controlador de Google Calendar
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import os
import json
from config import GOOGLE_SHEETS_CREDENTIALS_JSON, GOOGLE_CALENDAR_ID

SCOPES = ['https://www.googleapis.com/auth/calendar']

# En lugar de from_service_account_file, usamos from_service_account_info
# parseando el JSON que está en la variable GOOGLE_SHEETS_CREDENTIALS_JSON
info = json.loads(GOOGLE_SHEETS_CREDENTIALS_JSON)
creds = Credentials.from_service_account_info(info, scopes=SCOPES)

service = build('calendar', 'v3', credentials=creds)

def crear_evento(summary, start, end, description=None):
    evento = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start, 'timeZone': 'America/Mexico_City'},
        'end': {'dateTime': end, 'timeZone': 'America/Mexico_City'}
    }
    return service.events().insert(calendarId=GOOGLE_CALENDAR_ID, body=evento).execute()

def obtener_eventos_proximos(max_results=5):
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    eventos = service.events().list(calendarId=GOOGLE_CALENDAR_ID, timeMin=now,
                                    maxResults=max_results, singleEvents=True,
                                    orderBy='startTime').execute()
    return eventos.get('items', [])

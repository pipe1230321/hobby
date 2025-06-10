# Utilidades generales
import datetime

def formatear_fecha(fecha: datetime.datetime) -> str:
    return fecha.strftime('%d/%m/%Y %H:%M')

def limpiar_texto(texto: str) -> str:
    return texto.strip()

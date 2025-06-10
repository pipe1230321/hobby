# Controlador de Gemini AI
import requests
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_BASE_URL

def consulta_gemini(mensaje, contexto=None):
    url = f"{GEMINI_BASE_URL}/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": GEMINI_MODEL,
        "messages": [{"role": "user", "content": mensaje}],
        "temperature": 0.7
    }
    if contexto:
        data["messages"].extend(contexto)
    resp = requests.post(url, json=data, headers=headers)
    if resp.status_code == 200:
        return resp.json()['choices'][0]['message']['content']
    return "No se pudo obtener respuesta de Gemini."

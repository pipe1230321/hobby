# Controlador de voz: reconocimiento y síntesis
import speech_recognition as sr
from gtts import gTTS
import tempfile

def reconocer_voz(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    try:
        texto = r.recognize_google(audio, language='es-ES')
        return texto
    except Exception:
        return None

def texto_a_voz(texto):
    tts = gTTS(text=texto, lang='es')
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(temp.name)
    return temp.name

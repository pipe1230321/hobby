# Asistente Inteligente de Telegram

## Descripción
Bot modular en Python que integra:
- **Firebase Firestore/Storage**: usuarios, ingresos, gastos, tareas, notas y archivos adjuntos.
- **Google Sheets**: registro automático de movimientos.
- **Google Calendar**: creación y consulta de eventos.
- **Google Tasks**: gestión de tareas.
- **Gemini AI**: comprensión y sugerencias inteligentes.
- **Reconocimiento y síntesis de voz**: comandos y respuestas por audio.

## Ejemplos de comandos
- `/ingreso 1000 Sueldo Pago de nómina`
- `/gasto 200 Comida Almuerzo en restaurante`
- `/tarea Comprar leche`
- `/listar_tareas`
- `/completar_tarea <id>`
- `/evento Reunión con Juan mañana a las 10am`
- `/proximos_eventos`
- `/nota Recordar cita médica`
- `/consulta ¿Cuánto gasté este mes?`
- Enviar audio: el bot responde por voz.

## Flujo general
1. Usuario envía comando o audio.
2. El bot procesa y almacena en Firebase y Google.
3. Gemini AI sugiere, responde o extrae información.
4. El bot responde por texto o voz.

## Despliegue
1. Clona el repositorio y copia `.env.example` a `.env`.
2. Completa las variables de entorno:
   - Token de Telegram: [@BotFather](https://t.me/BotFather)
   - Firebase: crea proyecto, descarga JSON y bucket.
   - Google Cloud: activa APIs, descarga credenciales y configura IDs.
   - Gemini: consigue API key y URL base en [OpenRouter](https://openrouter.ai/).
3. Instala dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
4. Ejecuta el bot:
   ```powershell
   bash deploy.sh
   ```

## Plataformas gratuitas recomendadas
- [PythonAnywhere](https://www.pythonanywhere.com/)
- [Replit](https://replit.com/)
- [Railway](https://railway.app/)
- [Render](https://render.com/)

## Notas
- El bot y los mensajes están en español.
- Modular, escalable y fácil de mantener.
- Archivos adjuntos se almacenan en Firebase Storage.
- Puedes exportar datos desde Google Sheets.
- **IMPORTANTE:** Si usas Google Sheets, Calendar o Tasks, asegúrate de que la hora de tu sistema esté sincronizada con Internet. Si la hora está desfasada, Google rechazará la autenticación (error JWT/invalid_grant).

---

¿Dudas? Abre un issue o contacta al desarrollador.

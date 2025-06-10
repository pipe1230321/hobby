import logging
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from asistente_telegram.config import TELEGRAM_TOKEN
from asistente_telegram.controllers import firebase_controller, sheets_controller, calendar_controller, tasks_controller, gemini_controller, voice_controller, notas_controller
from utils import helpers
import os

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        firebase_controller.guardar_usuario(user.id, {"nombre": user.first_name})
        await update.message.reply_text(f"¡Hola {user.first_name}! Soy tu asistente inteligente. ¿En qué puedo ayudarte hoy?")
    except Exception as e:
        logging.error(f"Error en el comando /start: {e}")
        await update.message.reply_text("Hubo un problema al iniciar. Por favor, verifica tu configuración.")

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "🤖 *Comandos disponibles y ejemplos de uso:*\n\n"
        "/ingreso <monto> <categoría> <descripción>\n"
        "Ejemplo: /ingreso 1000 Sueldo Pago de nómina\n\n"
        "/gasto <monto> <categoría> <descripción>\n"
        "Ejemplo: /gasto 200 Comida Almuerzo en restaurante\n\n"
        "/tarea <texto>\n"
        "Ejemplo: /tarea Comprar leche\n\n"
        "/listar_tareas\n"
        "Muestra todas tus tareas pendientes.\n\n"
        "/completar_tarea <id>\n"
        "Ejemplo: /completar_tarea 123abc\n\n"
        "/evento <texto>\n"
        "Ejemplo: /evento Reunión con Juan mañana a las 10am\n\n"
        "/proximos_eventos\n"
        "Muestra tus próximos eventos del calendario.\n\n"
        "/nota <texto>\n"
        "Ejemplo: /nota Recordar cita médica\n\n"
        "/consulta <pregunta>\n"
        "Ejemplo: /consulta ¿Cuánto gasté este mes?\n\n"
        "🎙️ Comandos por voz:\n"
        "Envía un audio y el bot lo procesará como comando o consulta.\n\n"
        "Si tienes dudas, escribe /ayuda en cualquier momento."
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def ingreso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message:
            logging.error("El objeto update.message es None.")
            await update.effective_chat.send_message("Hubo un problema al procesar tu comando. Por favor, intenta nuevamente.")
            return

        if len(context.args) < 3:
            await update.message.reply_text("Uso: /ingreso <monto> <categoría> <descripción>")
            return

        try:
            monto = float(context.args[0])
        except ValueError:
            await update.message.reply_text("El monto debe ser un número válido.")
            return

        categoria = context.args[1]
        descripcion = ' '.join(context.args[2:])
        movimiento = {
            "tipo": "ingreso",
            "monto": monto,
            "categoria": categoria,
            "descripcion": descripcion,
            "fecha": helpers.formatear_fecha(update.message.date)
        }
        sheets_controller.agregar_movimiento(movimiento)
        await update.message.reply_text("Ingreso registrado correctamente.")
    except Exception as e:
        logging.error(f"Error en el comando /ingreso: {e}")
        await update.message.reply_text("Hubo un problema al procesar tu comando. Por favor, intenta nuevamente.")

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 3:
            await update.message.reply_text("Uso: /gasto <monto> <categoría> <descripción>")
            return

        try:
            monto = float(context.args[0])
        except ValueError:
            await update.message.reply_text("El monto debe ser un número válido.")
            return

        categoria = context.args[1]
        descripcion = ' '.join(context.args[2:])
        user_id = update.effective_user.id
        movimiento = {"tipo": "gasto", "monto": monto, "categoria": categoria, "descripcion": descripcion, "fecha": helpers.formatear_fecha(update.message.date)}
        firebase_controller.registrar_movimiento(user_id, movimiento)
        sheets_controller.registrar_movimiento_sheet(movimiento['fecha'], categoria, monto, descripcion)
        await update.message.reply_text("Gasto registrado correctamente.")
    except Exception as e:
        logging.error(f"Error en el comando /gasto: {e}")
        await update.message.reply_text("Hubo un problema al procesar tu comando. Por favor, verifica tu conexión e intenta nuevamente.")

async def tarea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("Uso: /tarea <texto>")
            return

        texto = ' '.join(context.args)
        user_id = update.effective_user.id
        firebase_controller.agregar_tarea(user_id, {"texto": texto, "completada": False, "tipo": "usuario"})
        tasks_controller.crear_tarea(texto)
        await update.message.reply_text("Tarea agregada.")
    except Exception as e:
        logging.error(f"Error en el comando /tarea: {e}")
        await update.message.reply_text("Hubo un problema al crear la tarea. Por favor, verifica tu conexión.")

async def listar_tareas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        tareas = tasks_controller.listar_tareas()
        if not tareas:
            await update.message.reply_text("No tienes tareas pendientes.")
        else:
            msg = "Tareas:\n" + '\n'.join([f"{t['id']}: {t['title']}" for t in tareas])
            await update.message.reply_text(msg)
    except Exception as e:
        logging.error(f"Error en el comando /listar_tareas: {e}")
        await update.message.reply_text("Hubo un problema al listar las tareas.")

async def completar_tarea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        task_id = context.args[0]
        tasks_controller.completar_tarea(task_id)
        await update.message.reply_text("Tarea completada.")
    except Exception as e:
        logging.error(f"Error en el comando /completar_tarea: {e}")
        await update.message.reply_text("Uso: /completar_tarea <id>")

async def evento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        texto = ' '.join(context.args)
        from datetime import datetime, timedelta
        ahora = datetime.now()
        inicio = ahora.isoformat()
        fin = (ahora + timedelta(hours=1)).isoformat()
        calendar_controller.crear_evento(texto, inicio, fin)
        await update.message.reply_text("Evento creado en tu calendario.")
    except Exception as e:
        logging.error(f"Error en el comando /evento: {e}")
        await update.message.reply_text("Uso: /evento <texto>")

async def proximos_eventos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        eventos = calendar_controller.obtener_eventos_proximos()
        if not eventos:
            await update.message.reply_text("No hay eventos próximos.")
        else:
            msg = "Próximos eventos:\n" + '\n'.join([f"{e['summary']} - {e['start'].get('dateTime', '')}" for e in eventos])
            await update.message.reply_text(msg)
    except Exception as e:
        logging.error(f"Error en el comando /proximos_eventos: {e}")
        await update.message.reply_text("Hubo un problema al obtener los eventos.")

async def voz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.voice or update.message.audio:
            archivo = await update.message.get_file()
            ruta = f"temp_{update.message.message_id}.ogg"
            await archivo.download_to_drive(ruta)
            texto = voice_controller.reconocer_voz(ruta)
            if texto:
                respuesta = gemini_controller.consulta_gemini(texto)
                audio_path = voice_controller.texto_a_voz(respuesta)
                with open(audio_path, 'rb') as audio:
                    await update.message.reply_voice(audio)
                os.remove(audio_path)
            else:
                await update.message.reply_text("No pude reconocer el audio.")
            os.remove(ruta)
        else:
            await update.message.reply_text("Envía un mensaje de voz o audio.")
    except Exception as e:
        logging.error(f"Error en el comando /voz: {e}")
        await update.message.reply_text("Hubo un problema al procesar el audio.")

async def nota(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("Uso: /nota <texto>")
            return

        texto = ' '.join(context.args)
        user_id = update.effective_user.id
        await notas_controller.agregar_nota(user_id, {"texto": texto, "fecha": helpers.formatear_fecha(update.message.date)})
        await update.message.reply_text("Nota guardada.")
    except Exception as e:
        logging.error(f"Error en el comando /nota: {e}")
        await update.message.reply_text("Hubo un problema al guardar la nota. Por favor, verifica tu conexión.")

async def consulta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pregunta = ' '.join(context.args)
        respuesta = gemini_controller.consulta_gemini(pregunta)
        await update.message.reply_text(respuesta)
    except Exception as e:
        logging.error(f"Error en el comando /consulta: {e}")
        await update.message.reply_text("Hubo un problema al realizar la consulta.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("ingreso", ingreso))
    app.add_handler(CommandHandler("gasto", gasto))
    app.add_handler(CommandHandler("tarea", tarea))
    app.add_handler(CommandHandler("listar_tareas", listar_tareas))
    app.add_handler(CommandHandler("completar_tarea", completar_tarea))
    app.add_handler(CommandHandler("evento", evento))
    app.add_handler(CommandHandler("proximos_eventos", proximos_eventos))
    app.add_handler(CommandHandler("nota", nota))
    app.add_handler(CommandHandler("consulta", consulta))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, voz))
    app.run_polling()

if __name__ == "__main__":
    main()

from telethon import TelegramClient, events
from datetime import datetime, timezone
import asyncio, threading, os
from flask import Flask

API_ID = 32695956
API_HASH = '8d939c8130ea03c01cd9abe6a6e83d7a'
SESSION = 'sesion_nube'
CANAL_ORIGEN = 'https://t.me/Horny_J'
# TU NUEVO DESTINO
GRUPO_DESTINO = -1003764262854
TOPIC_ID = 717696
# DESDE EL PRINCIPIO
DESDE_FECHA = datetime(2010, 1, 1, tzinfo=timezone.utc)
ARCHIVO_PROGRESO = "progreso.txt"

app = Flask(name)
@app.route('/')
def home():
    return "Bot vivo 24/7 sin duplicados"

def run_flask():
    app.run(host='0.0.0.0', port=10000)
threading.Thread(target=run_flask, daemon=True).start()

client = TelegramClient(SESSION, API_ID, API_HASH)

def guardar_progreso(msg_id):
    with open(ARCHIVO_PROGRESO, "w") as f:
        f.write(str(msg_id))

def leer_progreso():
    if os.path.exists(ARCHIVO_PROGRESO):
        try:
            with open(ARCHIVO_PROGRESO, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

async def copiar_historial():
    ultimo_id = leer_progreso()
    print(f"Ultimo ID copiado: {ultimo_id} - Copiando TODO desde el principio...")
    origen = await client.get_entity(CANAL_ORIGEN)
    destino = await client.get_entity(GRUPO_DESTINO)
    count = 0
    async for msg in client.iter_messages(origen, offset_date=DESDE_FECHA, reverse=True):
        if not msg: continue
        if msg.id <= ultimo_id:
            continue
        texto = (msg.text or "").strip()
        if not (msg.media or texto.startswith("https://telegra.ph")): continue
        try:
            if msg.media:
                await client.send_file(destino, msg.media, caption=msg.text, reply_to=TOPIC_ID)
            else:
                await client.send_message(destino, msg.text, reply_to=TOPIC_ID)
            guardar_progreso(msg.id)
            count += 1
            print(f"[{count}] Copiado {msg.id}")
            await asyncio.sleep(1.2)
        except Exception as e:
            print(e)
            await asyncio.sleep(3)
    print(f"Historial completo: {count} nuevos")

@client.on(events.NewMessage(chats=CANAL_ORIGEN))
async def handler(event):
    texto = (event.message.text or "").strip()
    if not (event.message.media or texto.startswith("https://telegra.ph")): return
    destino = await client.get_entity(GRUPO_DESTINO)
    try:
        if event.message.media:
            await client.send_file(destino, event.message.media, caption=event.message.text, reply_to=TOPIC_ID)
        else:
            await client.send_message(destino, event.message.text, reply_to=TOPIC_ID)
        guardar_progreso(event.message.id)
        print(f"Nuevo en vivo copiado: {event.message.id}")
    except Exception as e:
        print(e)

async def main():
    await client.start()
    await copiar_historial()
    print("BOT QUEDADO VIVO PARA SIEMPRE")
    await client.run_until_disconnected()

asyncio.run(main())

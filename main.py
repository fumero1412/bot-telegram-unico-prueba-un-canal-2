from telethon import TelegramClient, events
from telethon.sessions import StringSession
from datetime import datetime, timezone
import asyncio, threading, os
from flask import Flask

API_ID = 32695956
API_HASH = '8d939c8130ea03c01cd9abe6a6e83d7a'
SESSION_STRING = os.environ.get("SESSION_STRING")
CANAL_ORIGEN = 'https://t.me/Horny_J'
GRUPO_DESTINO = -1003764262854
TOPIC_ID = 717696
DESDE_FECHA = datetime(2010, 1, 1, tzinfo=timezone.utc)
ARCHIVO_PROGRESO = "progreso.txt"

app = Flask(name)
@app.route('/')
def home(): return "Bot vivo 24/7"
def run_flask(): app.run(host='0.0.0.0', port=10000)
threading.Thread(target=run_flask, daemon=True).start()

if not SESSION_STRING:
    print("ERROR: No hay SESSION_STRING en Environment!")
    client = TelegramClient('sesion_nube', API_ID, API_HASH)
else:
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

def guardar_progreso(m): 
    with open(ARCHIVO_PROGRESO, "w") as f: f.write(str(m))
def leer_progreso():
    if os.path.exists(ARCHIVO_PROGRESO):
        try:
            with open(ARCHIVO_PROGRESO, "r") as f: return int(f.read().strip())
        except: return 0
    return 0

async def copiar_historial():
    ultimo = leer_progreso()
    print(f"Conectando... Ultimo ID: {ultimo}")
    origen = await client.get_entity(CANAL_ORIGEN)
    destino = await client.get_entity(GRUPO_DESTINO)
    print(f"Origen: {origen.id} Destino: {destino.id} Topic: {TOPIC_ID}")
    async for msg in client.iter_messages(origen, offset_date=DESDE_FECHA, reverse=True):
        if not msg or msg.id <= ultimo: continue
        texto = (msg.text or "").strip()
        if not (msg.media or texto.startswith("https://telegra.ph")): continue
        try:
            if msg.media: await client.send_file(destino, msg.media, caption=msg.text, reply_to=TOPIC_ID)
            else: await client.send_message(destino, msg.text, reply_to=TOPIC_ID)
            guardar_progreso(msg.id)
            print(f"Copiado {msg.id}")
            await asyncio.sleep(1.2)
        except Exception as e:
            print(f"Error copiando {msg.id}: {e}")
            await asyncio.sleep(3)

@client.on(events.NewMessage(chats=CANAL_ORIGEN))
async def handler(event):
    texto = (event.message.text or "").strip()
    if not (event.message.media or texto.startswith("https://telegra.ph")): return
    destino = await client.get_entity(GRUPO_DESTINO)
    try:
        if event.message.media: await client.send_file(destino, event.message.media, caption=event.message.text, reply_to=TOPIC_ID)
        else: await client.send_message(destino, event.message.text, reply_to=TOPIC_ID)
        guardar_progreso(event.message.id)
        print(f"En vivo copiado: {event.message.id}")
    except Exception as e: print(f"Error vivo: {e}")

async def main():
    await client.start()
    print("CLIENTE CONECTADO OK")
    await copiar_historial()
    print("BOT QUEDADO VIVO")
    await client.run_until_disconnected()

asyncio.run(main())

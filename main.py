from telethon import TelegramClient, events
from datetime import datetime, timezone
import asyncio, threading, os
from flask import Flask

API_ID = 32695956
API_HASH = '8d939c8130ea03c01cd9abe6a6e83d7a'
SESSION = 'sesion_nube'
CANAL_ORIGEN = 'https://t.me/Horny_J'
GRUPO_DESTINO = 'https://t.me/+aH8ADmCchLYyNzNh'
TOPIC_ID = 713969
DESDE_FECHA = datetime(2022, 8, 7, 8, 38, 0, tzinfo=timezone.utc)

# --- Truco para que Render sea gratis ---
app = Flask(name)
@app.route('/')
def home():
    return "Bot vivo copiando desde 7 agosto 2022"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask, daemon=True).start()
# --- Fin truco ---

client = TelegramClient(SESSION, API_ID, API_HASH)

async def copiar_historial():
    print(f"Iniciando desde {DESDE_FECHA}...")
    origen = await client.get_entity(CANAL_ORIGEN)
    destino = await client.get_entity(GRUPO_DESTINO)
    count = 0
    async for msg in client.iter_messages(origen, offset_date=DESDE_FECHA, reverse=True):
        if not msg: continue
        texto = (msg.text or "").strip()
        tiene_media = msg.media is not None
        es_telegraph = texto.startswith("https://telegra.ph")
        if not tiene_media and not es_telegraph:
            continue
        try:
            if tiene_media:
                await client.send_file(destino, msg.media, caption=msg.text, reply_to=TOPIC_ID)
            else:
                await client.send_message(destino, msg.text, reply_to=TOPIC_ID)
            count += 1
            print(f"[{count}] {msg.id}")
            await asyncio.sleep(1.2)
        except Exception as e:
            print(e)
            await asyncio.sleep(3)
    print(f"Terminado: {count}")

@client.on(events.NewMessage(chats=CANAL_ORIGEN))
async def handler(event):
    texto = (event.message.text or "").strip()
    if not (event.message.media or texto.startswith("https://telegra.ph")):
        return
    destino = await client.get_entity(GRUPO_DESTINO)
    if event.message.media:
        await client.send_file(destino, event.message.media, caption=event.message.text, reply_to=TOPIC_ID)
    else:
        await client.send_message(destino, event.message.text, reply_to=TOPIC_ID)

async def main():
    await client.start()
    await copiar_historial()
    print("QUEDANDO VIVO")
    await client.run_until_disconnected()

asyncio.run(main())
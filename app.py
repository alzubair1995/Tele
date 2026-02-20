import os
import asyncio
import threading
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH", "")
TARGET_USERNAME = os.getenv("TG_TARGET", "")
SESSION_STRING = os.getenv("TG_SESSION_STRING", "")

def validate_env():
    missing = []
    if not API_ID:
        missing.append("TG_API_ID")
    if not API_HASH:
        missing.append("TG_API_HASH")
    if not TARGET_USERNAME:
        missing.append("TG_TARGET")
    if not SESSION_STRING:
        missing.append("TG_SESSION_STRING")
    if missing:
        raise RuntimeError(f"Missing env vars: {', '.join(missing)}")

async def telethon_worker():
    validate_env()
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        try:
            await event.forward_to(TARGET_USERNAME)
            print("✅ Message forwarded")
        except Exception as e:
            print("❌ Error:", e)

    print("🚀 Telethon worker started...")
    await client.start()
    await client.run_until_disconnected()

def start_telethon_in_thread():
    def runner():
        try:
            asyncio.run(telethon_worker())
        except Exception as e:
            print("❌ Telethon FATAL:", repr(e))
            raise

    t = threading.Thread(target=runner, daemon=True)
    t.start()

# --- Flask web server (for Render port binding) ---
app = Flask(__name__)

@app.get("/")
def home():
    return "OK - tele-swrt is running", 200

@app.get("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    start_telethon_in_thread()
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
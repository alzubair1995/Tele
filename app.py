import os
from telethon import TelegramClient, events

# قراءة المتغيرات من Environment Variables
API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
TARGET_USERNAME = os.getenv("TG_TARGET")
SESSION_NAME = os.getenv("TG_SESSION", "forward_session")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        await event.forward_to(TARGET_USERNAME)
        print("✅ Message forwarded")
    except Exception as e:
        print("❌ Error:", e)

async def main():
    print("🚀 Telegram Forwarder Started...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
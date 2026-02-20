import os
import asyncio
from telethon import TelegramClient, events

API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH", "")
TARGET_USERNAME = os.getenv("TG_TARGET", "")
SESSION_NAME = os.getenv("TG_SESSION", "forward_session")


def validate_env():
    missing = []
    if not API_ID:
        missing.append("TG_API_ID")
    if not API_HASH:
        missing.append("TG_API_HASH")
    if not TARGET_USERNAME:
        missing.append("TG_TARGET")
    if missing:
        raise RuntimeError(f"Missing env vars: {', '.join(missing)}")


async def main():
    validate_env()

    # إنشاء العميل داخل event loop
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        try:
            await event.forward_to(TARGET_USERNAME)
            print("✅ Message forwarded")
        except Exception as e:
            print("❌ Error:", e)

    print("🚀 Telegram Forwarder Started...")
    await client.start()  # سيطلب تسجيل دخول أول مرة
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
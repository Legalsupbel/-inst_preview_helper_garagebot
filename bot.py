import re
import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "8338246475:AAEjZVEarHk64tGrCaoP0HZA_SHgx4wF9GU"
ALLOWED_CHAT_ID = -1001889607662
# ===============================================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

INSTAGRAM_REGEX = re.compile(
    r'https?://(?:www\.)?instagram\.com/[^\s<>"\']+',
    re.IGNORECASE
)

def fix_instagram_link(url: str) -> str:
    """Заменяет www. на kk (получается kkinstagram.com)"""
    url = url.strip()
    url = re.sub(r'[.,;!?)\]]+$', '', url)

    if 'www.instagram.com' in url.lower():
        return re.sub(r'www\.instagram\.com', 'kkinstagram.com', url, flags=re.IGNORECASE)
    
    if 'instagram.com' in url.lower():
        return re.sub(r'(https?://)?instagram\.com', r'\1kkinstagram.com', url, flags=re.IGNORECASE)
    
    return url

@dp.message(Command("start"))
async def cmd_start(message: Message):
    if message.chat.id != ALLOWED_CHAT_ID:
        return
    await message.answer(
        "Бот работает.\n"
        "Просто кидайте Instagram-ссылки — я пришлю версию с предпросмотром."
    )

@dp.message(F.text)
async def handle_message(message: Message):
    if message.chat.id != ALLOWED_CHAT_ID:
        return

    text = message.text or ""
    matches = INSTAGRAM_REGEX.findall(text)

    if not matches:
        return

    fixed_links = []
    for link in matches:
        fixed = fix_instagram_link(link)
        if fixed.lower() != link.lower():
            fixed_links.append(fixed)

    if not fixed_links:
        return

    reply_text = "\n".join(fixed_links)

    try:
        await message.reply(reply_text, disable_web_page_preview=False)
    except Exception as e:
        logging.error(f"Ошибка отправки: {e}")

async def main():
    print("Бот запущен и работает...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
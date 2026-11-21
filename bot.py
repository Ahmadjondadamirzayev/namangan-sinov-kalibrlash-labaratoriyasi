import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Tokenni Render Environment Variables'dan oladi (agar yo'q bo'lsa, zaxira qiymat ishlatadi)
TOKEN = os.environ.get("BOT_TOKEN", "8935160715:AAESSqm9cy1YUaK34SeaovYhZBrXmcgAl-I")

bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔬 Uskunalar"),
                KeyboardButton(text="🛠 Xizmatlar"),
            ],
            [
                KeyboardButton(text="💰 Narxlar"),
                KeyboardButton(text="👤 Profil"),
            ],
            [
                KeyboardButton(text="ℹ️ Laboratoriya haqida"),
            ],
        ],
        resize_keyboard=True,
    )


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🏢 **Namangan Sinov va Kalibrlash Laboratoriyasi** konsultatsiya botiga xush kelibsiz!\n\n"
        "Kerakli bo'limni pastdagi tugmalar orqali tanlang:",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
    )


@dp.message(F.text.in_(["🔬 Uskunalar", "Uskunalar"]))
async def btn_equipment(message: types.Message):
    await message.answer(
        "🔬 **Laboratoriya uskunalari:**\n"
        "• Zamonaviy o'lchov va nazorat vositalari\n"
        "• Yuqori aniqlikdagi kalibrlash va sinov jihozlari",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
    )


@dp.message(F.text.in_(["🛠 Xizmatlar", "Xizmatlar", "/services"]))
async def btn_services(message: types.Message):
    await message.answer(
        "🛠 **Laboratoriya xizmatlari:**\n"
        "• Rezervuarlarni yuqori aniqlikda qiyoslash\n"
        "• O'lchash vositalarini sinash va kalibrlash\n"
        "• Rasmiy akkreditatsiyalangan xizmat",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
    )


@dp.message(F.text.in_(["💰 Narxlar", "Narxlar"]))
async def btn_prices(message: types.Message):
    await message.answer(
        "💰 **Xizmat narxlari bo'yicha konsultatsiya:**\n"
        "Narxlar uskuna turi, hajmi va ish murakkabligiga qarab belgilanadi.\n"
        "Aniq hisob-kitob uchun biz bilan bog'laning:\n"
        "📞 Telefon: +998996904779\n"
        "✉️ Email: muhammadyusufdadamirzayev@gmail.com",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
    )


@dp.message(F.text.in_(["👤 Profil", "Profil", "/profile"]))
async def btn_profile(message: types.Message):
    username = f"@{message.from_user.username}" if message.from_user.username else "Kiritilmagan"
    await message.answer(
        "👤 **Foydalanuvchi ma'lumotlari:**\n"
        f"• **ID:** `{message.from_user.id}`\n"
        f"• **Ism:** {message.from_user.first_name}\n"
        f"• **Username:** {username}",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
    )


@dp.message(F.text.in_(["ℹ️ Laboratoriya haqida", "Laboratoriya haqida", "/contact"]))
async def btn_about(message: types.Message):
    await message.answer(
        "ℹ️ **Namangan Sinov va Kalibrlash Laboratoriyasi**\n\n"
        "Biz sinov, qiyoslash va kalibrlash yo'nalishida ishonchli va sifatli xizmat ko'rsatamiz.\n"
        "📞 Telefon: +998996904779\n"
        "✉️ Email: muhammadyusufdadamirzayev@gmail.com",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
    )


async def health_check(request):
    return web.Response(text="Bot is running")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()


async def main():
    await start_web_server()
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

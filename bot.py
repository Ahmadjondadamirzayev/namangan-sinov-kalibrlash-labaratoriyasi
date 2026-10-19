
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# BotFather'dan olgan tokeningizni quyidagi qo'shtirnoq ichiga yozing
TOKEN = "8935160715:AAE0SlV-IgY8yVpzNBs-S7Lu6hUBxryrgQo"

# Vercel'dagi Mini App havolangiz
MINI_APP_URL = "https://namangan-lab.vercel.app"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_webapp_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🌐 Laboratoriya Ilovasini Ochish", 
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ],
        [
            InlineKeyboardButton(text="👤 Profil", callback_data="profile"),
            InlineKeyboardButton(text="📞 Aloqa", callback_data="contact")
        ]
    ])

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🏢 **Namangan Sinov va Kalibrlash Laboratoriyasi** rasmiy botiga xush kelibsiz!\n\n"
        "Quyidagi tugma orqali ilovamizni ochishingiz mumkin:",
        parse_mode="Markdown",
        reply_markup=get_webapp_keyboard()
    )

@dp.message(Command("app"))
async def cmd_app(message: types.Message):
    await message.answer(
        "🌐 **Mini App** orqali xizmatlardan foydalanish:",
        parse_mode="Markdown",
        reply_markup=get_webapp_keyboard()
    )

@dp.message(Command("services"))
async def cmd_services(message: types.Message):
    await message.answer(
        "🛠 **Laboratoriya xizmatlari:**\n"
        "• Rezervuarlarni yuqori aniqlikda qiyoslash\n"
        "• Rasmiy akkreditatsiyalangan xizmat",
        parse_mode="Markdown"
    )

@dp.message(Command("contact"))
async def cmd_contact(message: types.Message):
    await message.answer(
        "📞 **Aloqa ma'lumotlari:**\n"
        "Telefon: +998996904779\n"
        "Email: muhammadyusufdadamirzayev@gmail.com",
        parse_mode="Markdown"
    )

@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    await message.answer(
        f"👤 **Foydalanuvchi ma'lumotlari:**\nID: {message.from_user.id}\nIsm: {message.from_user.first_name}",
        parse_mode="Markdown"
    )

async def main():
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
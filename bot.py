import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

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


def get_equipment_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📏 Po'lat o'lchov lentasi va lotlar", callback_data="eq_tape")],
            [InlineKeyboardButton(text="📐 Lazerli masofa o'lchagich (Dalmomer)", callback_data="eq_laser")],
            [InlineKeyboardButton(text="🔭 Optik / Raqamli Nivelir va Teodolit", callback_data="eq_level")],
            [InlineKeyboardButton(text="🧪 Namunaviy o'lchov idishlari (Merniklar)", callback_data="eq_mernik")],
            [InlineKeyboardButton(text="🔊 Ultratovushli qalinlik o'lchagich", callback_data="eq_thickness")],
            [InlineKeyboardButton(text="🌡 Namunaviy termometr va areometrlar", callback_data="eq_thermo")],
            [InlineKeyboardButton(text="📊 Namunaviy manometrlar va bosim o'lchagichlar", callback_data="eq_manometer")],
            [InlineKeyboardButton(text="🛢 Rezervuarlar sotuvi (AYQSH, AGKSH, Neftbaza)", callback_data="eq_tanks")],
            [InlineKeyboardButton(text="📞 Mutaxassis bilan bog'lanish", url="https://t.me/DMYA_4779")],
        ]
    )


def get_profile_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📨 Telegram: @DMYA_4779", url="https://t.me/DMYA_4779")],
            [InlineKeyboardButton(text="📢 Telegram kanalimiz", url="https://t.me/Namangan_sinov_kalibrlash")],
            [InlineKeyboardButton(text="📸 Instagram (namangan_skl)", url="https://instagram.com/namangan_skl")],
        ]
    )


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🏢 **Namangan Sinov va Kalibrlash Laboratoriyasi** konsultatsiya botiga xush kelibsiz!\n\n"
        "Kerakli bo'limni pastdagi tugmalar orqali tanlang:",
        reply_markup=get_main_keyboard(),
    )


@dp.message(F.text.in_(["ℹ️ Laboratoriya haqida", "Laboratoriya haqida", "/about"]))
async def btn_about(message: types.Message):
    text = (
        "ℹ️ Laboratoriya haqida:\n\n"
        "«Namangan sinov va kalibrlash» sinov laboratoriyasi neft mahsulotlari, suv va boshqa suyuqliklarni "
        "saqlash rezervuarlarini qiyoslash hamda kalibrlash bo'yicha akkreditatsiyadan o'tgan rasmiy laboratoriya hisoblanadi.\n\n"
        "✅ Akkreditatsiya guvohnomasi: O'ZAK.QL.0149\n"
        "✅ Yuqori aniqlikdagi namunaviy o'lchash vositalari\n"
        "✅ Malakali metrolog mutaxassislar\n"
        "✅ Qonuniy asosdagi sertifikat va dalolatnomalar"
    )
    await message.answer(text, reply_markup=get_main_keyboard())


@dp.message(F.text.in_(["🛠 Xizmatlar", "Xizmatlar", "/services"]))
async def btn_services(message: types.Message):
    text = (
        "🛠 Bizning xizmatlarimiz:\n\n"
        "1️⃣ Gorizontal silindrik po'lat rezervuarlarni qiyoslash:\n"
        "- 0 m³ dan 200 m³ gacha — geometrik usulda\n"
        "- 0 m³ dan 25 m³ gacha — hajmiy usulda\n\n"
        "2️⃣ Vertikal silindrik po'lat rezervuarlarni qiyoslash:\n"
        "- 0 m³ dan 10 000 m³ gacha — geometrik usulda\n\n"
        "📜 Akkreditatsiya: O'ZAK davlat reestri: O'ZAK.QL.0149\n"
        "Barcha ishlar amaldagi davlat standartlari va me'yoriy talablar asosida amalga oshiriladi."
    )
    await message.answer(text, reply_markup=get_main_keyboard())


@dp.message(F.text.in_(["💰 Narxlar", "Narxlar", "/narxlar"]))
async def btn_prices(message: types.Message):
    text = (
        "💰 Xizmat narxlari:\n\n"
        "Rezervuarlarni qiyoslash va kalibrlash narxi quyidagi omillarga bog'liq:\n"
        "• Rezervuar turi (gorizontal yoki vertikal)\n"
        "• Rezervuar sig'imi (hajmi, m³)\n"

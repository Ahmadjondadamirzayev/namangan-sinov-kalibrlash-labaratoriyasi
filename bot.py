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


EQUIPMENT_DETAILS = {
    "eq_tape": "\n".join([
        "📏 Po'lat o'lchov lentasi va lotlar",
        "",
        "Rezervuarlarning geometrik o'lchamlarini va suyuqlik sathini yuqori aniqlikda o'lchash uchun davlat tekshiruvidan o'tgan namunaviy o'lchov lentalari va lotlari qo'llaniladi.",
    ]),
    "eq_laser": "\n".join([
        "📐 Lazerli masofa o'lchagich (Dalmomer)",
        "",
        "Rezervuar devorlari, balandligi va ichki geometrik parametrlarini tezkor hamda aniq o'lchash uchun zamonaviy lazerli masofa o'lchash vositasi.",
    ]),
    "eq_level": "\n".join([
        "🔭 Optik / Raqamli Nivelir va Teodolit",
        "",
        "Rezervuarlarning og'ishi, asosi holati va geometrik ko'rsatkichlarini geodezik/metrologik aniqlikda tekshirish uchun ishlatiladi.",
    ]),
    "eq_mernik": "\n".join([
        "🧪 Namunaviy o'lchov idishlari (Merniklar)",
        "",
        "Hajmiy usulda rezervuarlarni qiyoslash va o'lchash vositalarini tekshirish uchun sertifikatlangan namunaviy o'lchov idishlari.",
    ]),
    "eq_thickness": "\n".join([
        "🔊 Ultratovushli qalinlik o'lchagich",
        "",
        "Po'lat rezervuar devorlari va elementlarining qalinligini buzmaydigan usulda aniqlash uchun qo'llaniladi.",
    ]),
    "eq_thermo": "\n".join([
        "🌡 Namunaviy termometr va areometrlar",
        "",
        "Suyuqlik harorati va zichligini aniq o'lchash hamda qiyoslash ishlarida me'yoriy ko'rsatkichlarni ta'minlash uchun ishlatiladi.",
    ]),
    "eq_manometer": "\n".join([
        "📊 Namunaviy manometrlar va bosim o'lchagichlar",
        "",
        "Bosim o'lchash vositalarini tekshirish va kalibrlash jarayonlarida qo'llaniladigan yuqori aniqlikdagi namunaviy asboblar.",
    ]),
    "eq_tanks": "\n".join([
        "🛢 Rezervuarlar sotuvi (AYQSH, AGKSH

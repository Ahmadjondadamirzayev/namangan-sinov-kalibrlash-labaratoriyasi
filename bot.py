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
    "eq_tape": (
        "📏 Po'lat o'lchov lentasi va lotlar\n\n"
        "Rezervuarlarning geometrik o'lchamlarini va suyuqlik sathini yuqori aniqlikda "
        "o'lchash uchun davlat tekshiruvidan o'tgan namunaviy o'lchov lentalari va lotlari qo'llaniladi."
    ),
    "eq_laser": (
        "📐 Lazerli masofa o'lchagich (Dalmomer)\n\n"
        "Rezervuar devorlari, balandligi va ichki geometrik parametrlarini tezkor hamda aniq "
        "o'lchash uchun zamonaviy lazerli masofa o'lchash vositasi."
    ),
    "eq_level": (
        "🔭 Optik / Raqamli Nivelir va Teodolit\n\n"
        "Rezervuarlarning og'ishi, asosi holati va geometrik ko'rsatkichlarini geodezik/metrologik "
        "aniqlikda tekshirish uchun ishlatiladi."
    ),
    "eq_mernik": (
        "🧪 Namunaviy o'lchov idishlari (Merniklar)\n\n"
        "Hajmiy usulda rezervuarlarni qiyoslash va o'lchash vositalarini tekshirish uchun "
        "sertifikatlangan namunaviy o'lchov idishlari."
    ),
    "eq_thickness": (
        "🔊 Ultratovushli qalinlik o'lchagich\n\n"
        "Po'lat rezervuar devorlari va elementlarining qalinligini buzmaydigan usulda "
        "aniqlash uchun qo'llaniladi."
    ),
    "eq_thermo": (
        "🌡 Namunaviy termometr va areometrlar\n\n"
        "Suyuqlik harorati va zichligini aniq o'lchash hamda qiyoslash ishlarida me'yoriy "
        "ko'rsatkichlarni ta'minlash uchun ishlatiladi."
    ),
    "eq_manometer": (
        "📊 Namunaviy manometrlar va bosim o'lchagichlar\n\n"
        "Bosim o'lchash vositalarini tekshirish va kalibrlash jarayonlarida qo'llaniladigan "
        "yuqori aniqlikdagi namunaviy asboblar."
    ),
    "eq_tanks": (
        "🛢 Rezervuarlar sotuvi (AYQSH, AGKSH, Neftbaza)\n\n"
        "AYQSH, AGKSH va neftbazalar uchun rezervuarlar hamda ular bilan bog'liq masalalar "
        "bo'yicha batafsil ma'lumot olish uchun mutaxassis bilan bog'laning: @DMYA_4779."
    ),
}


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "🏢 Namangan Sinov va Kalibrlash Laboratoriyasi konsultatsiya botiga xush kelibsiz!\n\n"
        "Kerakli bo'limni pastdagi tugmalar orqali tanlang:"
    )
    await message.answer(text, reply_markup=get_main_keyboard())


@dp.message(F.text.in_(["ℹ️ Laboratoriya haqida", "Laboratoriya haqida", "/about"]))
async def btn_about(message: types.Message):
    text = (
        "ℹ️ Laboratoriya haqida:\n\n"
        "«Namangan sinov va kalibrlash» sinov laboratoriyasi neft mahsulotlari, suv va boshqa "
        "suyuqliklarni saqlash rezervuarlarini qiyoslash hamda kalibrlash bo'yicha "
        "akkreditatsiyadan o'tgan rasmiy laboratoriya hisoblanadi.\n\n"
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
        "• O'lchash usuli (geometrik yoki hajmiy)\n"
        "• Obyektning joylashgan hududi\n\n"
        "ℹ️ Aniq hisob-kitob va tijoriy taklif olish uchun @DMYA_4779 yoki +998996904779 orqali bog'laning."
    )
    await message.answer(text, reply_markup=get_main_keyboard())


@dp.message(F.text.in_(["🔬 Uskunalar", "Uskunalar", "/uskunalar"]))
async def btn_equipment(message: types.Message):
    text = (
        "🔬 O'lchash va kalibrlash uskunalari\n\n"
        "Bizning laboratoriyamizda barcha sinov va qiyoslash ishlari davlat metrologiya "
        "tekshiruvidan o'tgan zamonaviy va yuqori aniqlikdagi uskunalar yordamida olib boriladi.\n\n"
        "Batafsil ma'lumot olish uchun quyidagi uskunalardan birini tanlang:"
    )
    await message.answer(text, reply_markup=get_equipment_keyboard())


@dp.callback_query(F.data.in_(EQUIPMENT_DETAILS.keys()))
async def cb_equipment_detail(callback: types.CallbackQuery):
    detail_text = EQUIPMENT_DETAILS[callback.data]
    back_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📞 Mutaxassis bilan bog'lanish", url="https://t.me/DMYA_4779")],
            [InlineKeyboardButton(text="⬅️ Uskunalar ro'yxatiga qaytish", callback_data="back_to_equipment")],
        ]
    )
    await callback.message.answer(detail_text, reply_markup=back_kb)
    await callback.answer()


@dp.callback_query(F.data == "back_to_equipment")
async def cb_back_to_equipment(callback: types.CallbackQuery):
    text = (
        "🔬 O'lchash va kalibrlash uskunalari\n\n"
        "Bizning laboratoriyamizda barcha sinov va qiyoslash ishlari davlat metrologiya "
        "tekshiruvidan o'tgan zamonaviy va yuqori aniqlikdagi uskunalar yordamida olib boriladi.\n\n"
        "Batafsil ma'lumot olish uchun quyidagi uskunalardan birini tanlang:"
    )
    await callback.message.answer(text, reply_markup=get_equipment_keyboard())
    await callback.answer()


@dp.message(F.text.in_(["👤 Profil", "Profil", "/profile"]))
async def btn_profile(message: types.Message):
    text = (
        "🏢 «Namangan sinov va kalibrlash» laboratoriyasi\n\n"
        "👤 Profil / Bog'lanish:\n"
        "✈️ Telegram: @DMYA_4779\n"
        "📞 Telefon: +998996904779\n"
        "✉️ Email: muhammadyusufdadamirzayev@gmail.com\n\n"
        "🌐 Bizning ijtimoiy tarmoqlarimiz:\n"
        "📣 Telegram kanal: t.me/Namangan_sinov_kalibrlash\n"
        "📸 Instagram: namangan_skl\n\n"
        "📍 Manzil: Namangan shahri, Nodira ko'chasi, 9-uy\n"
        "🕒 Ish vaqti: Dushanba — Shanba, 09:00 dan 18:00 gacha"
    )
    await message.answer(text, reply_markup=get_profile_keyboard())


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

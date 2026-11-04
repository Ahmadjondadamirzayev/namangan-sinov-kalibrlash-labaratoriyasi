import asyncio
import os
from typing import Dict, Any

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

try:
    from anthropic import AsyncAnthropic
except ImportError:
    AsyncAnthropic = None

# --- SOZLAMALAR ------------------------------------------------------------
TOKEN = os.getenv("BOT_TOKEN", "8935160715:AAEJHKsszG1re3aBA8V43-Yf3xZpsebjthU")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
AI_MODEL = "claude-haiku-5-5"

# --- MA'LUMOTLAR ----------------------------------------------------------
PROFIL = (
    "🏢 <b>«Namangan sinov va kalibrlash» laboratoriyasi</b>\n\n"
    "👤 <b>Profil / Bog'lanish:</b>\n"
    "✈️ <b>Telegram:</b> @DMYA_4779\n"
    "📞 <b>Telefon:</b> +998996904779\n"
    "📧 <b>Email:</b> muhammadyusufdadamirzayev@gmail.com\n\n"
    "🌐 <b>Bizning ijtimoiy tarmoqlarimiz:</b>\n"
    "📢 <b>Telegram kanal:</b> <a href=\"https://t.me/Namangan_sinov_kalibrlash\">t.me/Namangan_sinov_kalibrlash</a>\n"
    "📸 <b>Instagram:</b> <a href=\"https://instagram.com/namangan_skl\">namangan_skl</a>\n\n"
    "📍 <b>Manzil:</b> Namangan shahri, Nodira ko'chasi, 9-uy\n"
    "🕒 <b>Ish vaqti:</b> Dushanba — Shanba, 09:00 dan 18:00 gacha"
)

XIZMATLAR = (
    "🛠 <b>Bizning xizmatlarimiz:</b>\n\n"
    "1️⃣ <b>Gorizontal silindrik po'lat rezervuarlarni qiyoslash:</b>\n"
    "   • 0 m³ dan 200 m³ gacha — geometrik usulda\n"
    "   • 0 m³ dan 25 m³ gacha — hajmiy usulda\n\n"
    "2️⃣ <b>Vertikal silindrik po'lat rezervuarlarni qiyoslash:</b>\n"
    "   • 0 m³ dan 10 000 m³ gacha — geometrik usulda\n\n"
    "📜 <b>Akkreditatsiya:</b> O'ZAK davlat reestri: <code>O'ZAK.QL.0149</code>\n"
    "Barcha ishlar amaldagi davlat standartlari va me'yoriy talablar asosida amalga oshiriladi."
)

NARXLAR = (
    "💰 <b>Xizmat narxlari:</b>\n\n"
    "Rezervuarlarni qiyoslash va kalibrlash narxi quyidagi omillarga bog'liq:\n"
    "• Rezervuar turi (gorizontal yoki vertikal)\n"
    "• Rezervuar sig'imi (hajmi, m³)\n"
    "• O'lchash usuli (geometrik yoki hajmiy)\n"
    "• Obyektning joylashgan hududi\n\n"
    "ℹ️ Aniq hisob-kitob va tijoriy taklif olish uchun @DMYA_4779 yoki +998996904779 orqali bog'laning."
)

LABORATORIYA_HAQIDA = (
    "ℹ️ <b>Laboratoriya haqida:</b>\n\n"
    "«Namangan sinov va kalibrlash» sinov laboratoriyasi neft mahsulotlari, "
    "suv va boshqa suyuqliklarni saqlash rezervuarlarini qiyoslash hamda "
    "kalibrlash bo'yicha akkreditatsiyadan o'tgan rasmiy laboratoriya hisoblanadi.\n\n"
    "✅ <b>Akkreditatsiya guvohnomasi:</b> <code>O'ZAK.QL.0149</code>\n"
    "✅ Yuqori aniqlikdagi namunaviy o'lchash vositalari\n"
    "✅ Malakali metrolog mutaxassislar\n"
    "✅ Qonuniy asosdagi sertifikat va dalolatnomalar"
)

# --- USKUNALAR MA'LUMOTLAR BAZASI ---------------------------------------
USKUNALAR: Dict[str, Dict[str, str]] = {
    "lenta": {
        "nomi": "📏 Po'lat o'lchov lentasi va lotlar",
        "tavsif": (
            "📏 <b>Po'lat o'lchov lentasi va og'irlik lotlari</b>\n\n"
            "🔹 <b>Vazifasi:</b> Rezervuarlarning balandligi, suyuqlik sathi (neft, yoqilg'i va h.k.) hamda "
            "tashqi va ichki o'lchamlarini millimetrgacha aniqlikda o'lchash.\n"
            "🔹 <b>Qo'llanilishi:</b> Gorizontal va vertikal rezervuarlarni geometrik usulda qiyoslashda.\n"
            "🔹 <b>Xususiyatlari:</b> 2-toifali yuqori aniqlikdagi davlat metrologiya tekshiruvidan o'tgan po'lat lenta."
        ),
    },
    "lazer": {
        "nomi": "📐 Lazerli masofa o'lchagich (Dalmomer)",
        "tavsif": (
            "📐 <b>Lazerli masofa o'lchagich (Lazer dalmomer)</b>\n\n"
            "🔹 <b>Vazifasi:</b> Rezervuarlar ichki va tashqi diametrlari, balandliklari hamda masofalarni kontaktsiz tezkor o'lchash.\n"
            "🔹 <b>Qo'llanilishi:</b> Katta hajmli (100–10 000 m³) vertikal rezervuarlarning geometrik parametrlarini aniqlashda.\n"
            "🔹 <b>Xususiyatlari:</b> ±1 mm aniqlik, 100 metrgacha masofani o'lchash imkoniyati."
        ),
    },
    "nivelir": {
        "nomi": "🔭 Optik / Raqamli Nivelir va Teodolit",
        "tavsif": (
            "🔭 <b>Optik va raqamli geodezik nivelir</b>\n\n"
            "🔹 <b>Vazifasi:</b> Rezervuarlar tagi (tubi)ning notekisligi, deformatsiyasi va vertikal o'qdan og'ishini aniqlash.\n"
            "🔹 <b>Qo'llanilishi:</b> Rezervuarlarni montajdan keyin va davriy qiyoslash jarayonlarida xatoliklarni hisobga olish.\n"
            "🔹 <b>Xususiyatlari:</b> Yuqori kattalashtirish darajasi va kompensatorli aniqlik."
        ),
    },
    "mernik": {
        "nomi": "🧪 Namunaviy o'lchov idishlari (Merniklar)",
        "tavsif": (
            "🧪 <b>Namunaviy ikkinchi toifali o'lchov idishlari (Merniklar)</b>\n\n"
            "🔹 <b>Vazifasi:</b> Suyuqlik hajmini aniq dozalash va rezervuarlarni hajmiy (dinamik) usulda qiyoslash.\n"
            "🔹 <b>Qo'llanilishi:</b> 3–25 m³ gacha bo'lgan gorizontal rezervuarlar va yoqilg'i tarqatish ustunlarini tekshirishda.\n"
            "🔹 <b>Xususiyatlari:</b> Shkalali bo'yin va termo-optik ko'rsatkichlar bilan jihozlangan."
        ),
    },
    "tolshinomer": {
        "nomi": "🔍 Ultratovushli qalinlik o'lchagich",
        "tavsif": (
            "🔍 <b>Ultratovushli qalinlik o'lchagich (Tolshinomer)</b>\n\n"
            "🔹 <b>Vazifasi:</b> Rezervuar devorlari va tubi metallining qalinligini, korroziyaga uchrash darajasini o'lchash.\n"
            "🔹 <b>Qo'llanilishi:</b> Rezervuarning texnik holatini baholash va haqiqiy ichki hajmini to'g'ri hisoblashda.\n"
            "🔹 <b>Xususiyatlari:</b> 0.01 mm aniqlikdagi raqamli zond."
        ),
    },
    "termometr": {
        "nomi": "🌡 Namunaviy termometr va areometrlar",
        "tavsif": (
            "🌡 <b>Namunaviy termometr va areometrlar jamlanmasi</b>\n\n"
            "🔹 <b>Vazifasi:</b> Rezervuar ichidagi suyuqlik harorati va zichligini o'lchash.\n"
            "🔹 <b>Qo'llanilishi:</b> Hajmiy usulda qiyoslash paytida harorat ta'siridagi hajm kengayishini hisobga olish.\n"
            "🔹 <b>Xususiyatlari:</b> 0.1 °C va 0.5 kg/m³ aniqlikdagi davlat tekshiruvidan o'tgan asboblar."
        ),
    },
    "manometr": {
        "nomi": "📊 Namunaviy manometrlar va bosim o'lchagichlar",
        "tavsif": (
            "📊 <b>Namunaviy manometrlar va bosim datchiklari</b>\n\n"
            "🔹 <b>Vazifasi:</b> Rezervuarlar, quvurlar va klapanlardagi bosimni o'lchash hamda sinash.\n"
            "🔹 <b>Qo'llanilishi:</b> Bosim ostida ishlovchi sig'imlarni texnik sinovdan o'tkazishda.\n"
            "🔹 <b>Xususiyatlari:</b> 0.4 va 0.25 aniqlik sinfiga ega yuqori sifatli manometrlar."
        ),
    },
    "rezervuar_sotish": {
        "nomi": "🛢 Rezervuarlar sotuvi (AYQSH, AGKSH, Neftbaza)",
        "tavsif": (
            "🛢 <b>AYQSH, AGKSH va neftbazalarda ishlatiladigan rezervuarlarni sotish</b>\n\n"
            "🔹 <b>Mahsulotlar:</b> AYQSH, AGKSH va neftbazalar uchun har xil sig'imdagi sifatli po'lat rezervuarlar (gorizontal va vertikal).\n"
            "🔹 <b>Qo'llanilishi:</b> Neft mahsulotlari, yonilg'i, gaz va texnik suyuqliklarni xavfsiz saqlash.\n"
            "🔹 <b>Sifati:</b> Davlat standartlariga to'liq javob beruvchi mustahkam sig'imlar.\n\n"
            "📞 <b>Buyurtma berish:</b> @DMYA_4779 (+998996904779)"
        ),
    },
}

# --- TUGMALAR (KLAVIATURALAR) ----------------------------------------------
MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔬 Uskunalar"), KeyboardButton(text="🛠 Xizmatlar")],
        [KeyboardButton(text="💰 Narxlar"), KeyboardButton(text="👤 Profil")],
        [KeyboardButton(text="ℹ️ Laboratoriya haqida")],
    ],
    resize_keyboard=True,
)


def get_profil_keyboard() -> InlineKeyboardMarkup:
    """Profil va bog'lanish uchun inline tugmalar"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✈️ Telegram: @DMYA_4779", url="https://t.me/DMYA_4779")],
            [InlineKeyboardButton(text="📢 Telegram kanalimiz", url="https://t.me/Namangan_sinov_kalibrlash")],
            [InlineKeyboardButton(text="📸 Instagram (namangan_skl)", url="https://instagram.com/namangan_skl")],
        ]
    )


def get_uskunalar_keyboard() -> InlineKeyboardMarkup:
    """Uskunalar ro'yxatini inline tugmalar ko'rinishida chiqarish"""
    buttons = []
    for key, data in USKUNALAR.items():
        buttons.append([InlineKeyboardButton(text=data["nomi"], callback_data=f"uskuna:{key}")])
    buttons.append([
        InlineKeyboardButton(text="📞 Mutaxassis bilan bog'lanish", url="https://t.me/DMYA_4779")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_uskuna_detail_keyboard() -> InlineKeyboardMarkup:
    """Alohida uskuna ko'rilayotganda ortga qaytish tugmalari"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Barcha uskunalarga qaytish", callback_data="uskunalar:all")],
            [InlineKeyboardButton(text="📞 Buyurtma berish / Savol yo'llash", url="https://t.me/DMYA_4779")],
        ]
    )


# --- MATN TEKSHIRUVCHISI --------------------------------------------------
JAVOBLAR = [
    (["narx", "qancha", "necha pul", "to'lov", "tarif", "baho"], NARXLAR),
    (["xizmat", "nima qilasiz", "qiyoslash", "kalibrlash", "rezervuar", "sig'im"], XIZMATLAR),
    (["profil", "bog'lan", "aloqa", "telefon", "raqam", "admin", "manzil", "email", "pochta"], PROFIL),
    (["laboratoriya", "akkreditatsiya", "haqida", "guvohnoma", "litsenziya"], LABORATORIYA_HAQIDA),
    (["salom", "assalom", "qalaysiz", "salomaleykum", "start"],
     "Assalomu alaykum! 👋\n«Namangan sinov va kalibrlash» botiga xush kelibsiz! Kerakli bo'limni tanlang:"),
]

FALLBACK = (
    "Xabaringiz qabul qilindi! 🙏\n\n"
    "Quyidagi menyudan kerakli bo'limni tanlashingiz yoki to'g'ridan-to'g'ri bog'lanishingiz mumkin:\n"
    "✈️ <b>Telegram:</b> @DMYA_4779\n"
    "📞 <b>Telefon:</b> +998996904779\n"
    "📧 <b>Email:</b> muhammadyusufdadamirzayev@gmail.com\n\n"
    "🌐 <b>Ijtimoiy tarmoqlarimiz:</b>\n"
    "📢 Telegram kanal: <a href=\"https://t.me/Namangan_sinov_kalibrlash\">t.me/Namangan_sinov_kalibrlash</a>\n"
    "📸 Instagram: <a href=\"https://instagram.com/namangan_skl\">namangan_skl</a>"
)

AI_SYSTEM = f"""Sen «Namangan sinov va kalibrlash» laboratoriyasining professional, muloyim va yordam beruvchi virtual assistentisan.

Laboratoriya ma'lumotlari:
{XIZMATLAR}

{NARXLAR}

{PROFIL}

{LABORATORIYA_HAQIDA}

Qoidalar:
- Faqat o'zbek tilida, xushmuomala va aniq javob ber.
- Barcha javoblaring laboratoriya faoliyati, rezervuarlarni qiyoslash, kalibrlash va o'lchov uskunalariga tegishli bo'lsin.
- O'zingdan narx yoki asossiz ma'lumot to'qima. Aniq narx yoki kelishuv uchun @DMYA_4779 ga murojaat qilishni taklif qil.
"""

ai = AsyncAnthropic(api_key=ANTHROPIC_KEY) if (AsyncAnthropic and ANTHROPIC_KEY) else None
dp = Dispatcher()


async def get_reply(matn: str) -> str:
    """1) tayyor kalit so'zlar  2) AI yordamchi  3) standart javob"""
    low = matn.lower()
    for kalitlar, javob in JAVOBLAR:
        if any(k in low for k in kalitlar):
            return javob

    if ai:
        try:
            r = await ai.messages.create(
                model=AI_MODEL,
                max_tokens=400,
                system=AI_SYSTEM,
                messages=[{"role": "user", "content": matn}],
            )
            return r.content[0].text
        except Exception as e:
            print("AI xatosi:", e)

    return FALLBACK


# --- ASOSIY BUYRUQLAR VA HANDLERLAR ----------------------------------------
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 <b>Assalomu alaykum!</b>\n\n"
        "«Namangan sinov va kalibrlash» laboratoriyasining rasmiy botiga xush kelibsiz.\n\n"
        "Bu yerda siz bizning xizmatlarimiz, qo'llaniladigan uskunalar, narxlar va laboratoriya "
        "ma'lumotlari bilan tanishishingiz mumkin.\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang 👇",
        parse_mode="HTML",
        reply_markup=MENU,
    )


@dp.message(Command("uskunalar"))
@dp.message(F.text == "🔬 Uskunalar")
async def uskunalar_handler(message: Message):
    matn = (
        "🔬 <b>O'lchash va kalibrlash uskunalari</b>\n\n"
        "Bizning laboratoriyamizda barcha sinov va qiyoslash ishlari davlat metrologiya "
        "tekshiruvidan o'tgan zamonaviy va yuqori aniqlikdagi uskunalar yordamida olib boriladi.\n\n"
        "Batafsil ma'lumot olish uchun quyidagi uskunalardan birini tanlang:"
    )
    await message.answer(matn, parse_mode="HTML", reply_markup=get_uskunalar_keyboard())


@dp.callback_query(F.data == "uskunalar:all")
async def uskunalar_callback_all(callback: CallbackQuery):
    matn = (
        "🔬 <b>O'lchash va kalibrlash uskunalari</b>\n\n"
        "Kerakli uskunani tanlang va uning vazifasi hamda xususiyatlari bilan tanishing:"
    )
    if callback.message:
        try:
            await callback.message.edit_text(
                matn,
                parse_mode="HTML",
                reply_markup=get_uskunalar_keyboard(),
            )
        except Exception:
            pass
    await callback.answer()


@dp.callback_query(F.data.startswith("uskuna:"))
async def uskuna_detail_callback(callback: CallbackQuery):
    uskuna_key = callback.data.split(":")[1]
    data = USKUNALAR.get(uskuna_key)

    if not data:
        await callback.answer("Uskuna haqida ma'lumot topilmadi.", show_alert=True)
        return

    if callback.message:
        try:
            await callback.message.edit_text(
                data["tavsif"],
                parse_mode="HTML",
                reply_markup=get_uskuna_detail_keyboard(),
            )
        except Exception:
            pass
    await callback.answer()


@dp.message(Command("xizmatlar"))
@dp.message(F.text == "🛠 Xizmatlar")
async def xizmatlar_handler(message: Message):
    await message.answer(XIZMATLAR, parse_mode="HTML", reply_markup=MENU)


@dp.message(Command("narxlar"))
@dp.message(F.text == "💰 Narxlar")
async def narxlar_handler(message: Message):
    await message.answer(NARXLAR, parse_mode="HTML", reply_markup=MENU)


@dp.message(Command("profil"))
@dp.message(Command("profile"))
@dp.message(Command("aloqa"))
@dp.message(Command("contact"))
@dp.message(F.text.in_({"👤 Profil", "👤 Bog'lanish / Profil", "Profil", "profil"}))
async def profil_handler(message: Message):
    await message.answer(PROFIL, parse_mode="HTML", reply_markup=get_profil_keyboard())


@dp.message(Command("haqida"))
@dp.message(F.text == "ℹ️ Laboratoriya haqida")
async def haqida_handler(message: Message):
    await message.answer(LABORATORIYA_HAQIDA, parse_mode="HTML", reply_markup=MENU)


# Matnli xabarlar uchun umumiy qabul qiluvchi
@dp.message(F.text)
async def text_message_handler(message: Message):
    text = message.text.strip().lower()

    if any(k in text for k in ["uskuna", "asbob", "pribor", "qurilma", "instrument"]):
        await uskunalar_handler(message)
        return

    reply_text = await get_reply(message.text)
    await message.answer(reply_text, parse_mode="HTML", reply_markup=MENU)


# --- TELEGRAM BUSINESS FUNKSIYASI ------------------------------------------
_owners: dict[str, int] = {}


async def owner_id(bot: Bot, conn_id: str) -> int:
    if conn_id not in _owners:
        conn = await bot.get_business_connection(conn_id)
        _owners[conn_id] = conn.user.id
    return _owners[conn_id]


@dp.business_message()
async def business_msg(message: Message, bot: Bot):
    if not message.text:
        return
    # O'zingiz yozgan xabarlarga bot javob bermasin
    if message.from_user and message.from_user.id == await owner_id(bot, message.business_connection_id):
        return
    await message.answer(await get_reply(message.text), parse_mode="HTML")


# --- ASOSIY ISHGA TUSHIRISH FUNKSIYASI -------------------------------------
async def main():
    bot = Bot(TOKEN)
    await bot.set_my_commands([
        BotCommand(command="start", description="Botni qayta ishga tushirish"),
        BotCommand(command="uskunalar", description="O'lchash va kalibrlash uskunalari"),
        BotCommand(command="xizmatlar", description="Laboratoriya xizmatlari"),
        BotCommand(command="narxlar", description="Narxlar va tariflar"),
        BotCommand(command="profil", description="Bog'lanish va manzil"),
        BotCommand(command="haqida", description="Akkreditatsiya va ma'lumot"),
    ])
    print("==================================================")
    print("«Namangan sinov va kalibrlash» boti muvaffaqiyatli ishga tushdi!")
    print(f"AI holati: {'Yoqilgan' if ai else 'Ochiq (ixtiyoriy)'}")
    print("==================================================")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

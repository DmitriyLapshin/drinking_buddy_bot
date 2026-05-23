import os
import asyncio
import random
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web
import aiosqlite

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("❌ Ошибка: Переменная BOT_TOKEN не найдена в окружении")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
DB_FILE = "sobutylbnik.db"

# ================= 100 ОСТРЫХ/ГОРЯЧИХ ТОСТОВ =================
TOASTS = [
    "За тех, кто не ждёт идеального момента, а создаёт его сам.",
    "Пусть ночь будет долгой, а утро — без лишних оправданий.",
    "За тех, кто пьёт не чтобы спрятаться, а чтобы раскрыться.",
    "Чтобы желания не оставались в черновиках, а воплощались в реальности.",
    "За тех, кто не боится быть неудобным, но остаётся честным.",
    "Пусть каждый тост будет не формальностью, а признанием.",
    "За смелость сказать «да», когда все ждут «нет».",
    "Чтобы в бокале была не просто жидкость, а настроение.",
    "За тех, кто не коллекционирует людей, а ценит моменты.",
    "Пусть правила будут мягкими, а ночи — жаркими.",
    "За тех, кто не извиняется за свой аппетит к жизни.",
    "Чтобы страсть не выгорала, а разгоралась с каждым глотком.",
    "За тех, кто не играет по чужим правилам, а пишет свои.",
    "Пусть в голове будет ясно, а в сердце — горячо.",
    "За тех, кто не боится ошибиться, но боится не попробовать.",
    "Чтобы каждый вечер оставлял историю, а не пустоту.",
    "За тех, кто не прячет характер за улыбкой.",
    "Пусть выбор будет осознанным, а последствия — приятными.",
    "За тех, кто не ждёт разрешения, чтобы быть счастливым.",
    "Чтобы в речи не было фальши, а в поступках — ясности.",
    "За тех, кто не путает свободу с вседозволенностью.",
    "Пусть ночь будет щедрой, а утро — честным.",
    "За тех, кто не боится быть громким, когда вокруг тихо.",
    "Чтобы каждый тост зажигал, а не гасил.",
    "За тех, кто не коллекционирует обещания, а выполняет их.",
    "Пусть в бокале будет огонь, а в груди — спокойствие.",
    "За тех, кто не ждёт знака свыше, а сам его создаёт.",
    "Чтобы страсть не уходила в прошлое, а жила в настоящем.",
    "За тех, кто не боится быть первым, кто протянет руку.",
    "Пусть каждый вечер будет экспериментом, а не обязанностью.",
    "За тех, кто не прячет свои слабости, а делает их силой.",
    "Чтобы в жизни было больше «хочу» и меньше «надо».",
    "За тех, кто не играет в безопасные игры, а рискует красиво.",
    "Пусть ночь помнит нас, а утро не осуждает.",
    "За тех, кто не ждёт идеальных условий, а создаёт их здесь и сейчас.",
    "Чтобы каждый глоток был выбором, а не автоматизмом.",
    "За тех, кто не боится быть неудобным, но остаётся верным себе.",
    "Пусть в словах будет пряность, а в делах — точность.",
    "За тех, кто не коллекционирует лайки, а ценит взгляды.",
    "Чтобы страсть не выдыхалась, а разгоралась с каждым тостом.",
    "За тех, кто не ждёт разрешения, чтобы быть собой.",
    "Пусть ночь будет щедрой, а утро — без лишних вопросов.",
    "За тех, кто не прячет характер за вежливостью.",
    "Чтобы каждый вечер оставлял шрам, а не синяк.",
    "За тех, кто не боится быть первым, кто скажет «хватит» или «ещё».",
    "Пусть в бокале будет не просто напиток, а состояние.",
    "За тех, кто не играет по чужим сценариям, а пишет свои.",
    "Чтобы страсть не уходила в тень, а выходила на свет.",
    "За тех, кто не ждёт знака, а сам его зажигает.",
    "Пусть каждый тост будет не формальностью, а признанием в смелости.",
    "За тех, кто не боится быть громким, когда мир шепчет.",
    "Чтобы в жизни было больше огня и меньше воды.",
    "За тех, кто не коллекционирует отговорки, а делает шаги.",
    "Пусть ночь будет долгой, а утро — без сожалений.",
    "За тех, кто не прячет свои желания за «потом».",
    "Чтобы каждый глоток был решением, а не привычкой.",
    "За тех, кто не боится быть неудобным, но остаётся честным.",
    "Пусть в словах будет жар, а в поступках — ясность.",
    "За тех, кто не ждёт идеального момента, а создаёт его.",
    "Чтобы страсть не гасла, а тлела до нового огня.",
    "За тех, кто не играет в безопасные игры, а рискует красиво.",
    "Пусть каждый вечер будет экспериментом, а не рутиной.",
    "За тех, кто не прячет характер за улыбкой.",
    "Чтобы в бокале был не просто алкоголь, а настрой.",
    "За тех, кто не ждёт разрешения, чтобы быть счастливым.",
    "Пусть ночь помнит нас, а утро не осуждает.",
    "За тех, кто не коллекционирует обещания, а выполняет их.",
    "Чтобы страсть не уходила в прошлое, а жила в настоящем.",
    "За тех, кто не боится быть первым, кто протянет руку.",
    "Пусть каждый тост зажигает, а не гасит.",
    "За тех, кто не путает свободу с вседозволенностью.",
    "Чтобы в жизни было больше «хочу» и меньше «надо».",
    "За тех, кто не прячет свои слабости, а делает их силой.",
    "Пусть ночь будет щедрой, а утро — честным.",
    "За тех, кто не ждёт знака свыше, а сам его создаёт.",
    "Чтобы каждый вечер оставлял шрам, а не синяк.",
    "За тех, кто не боится быть громким, когда вокруг тихо.",
    "Пусть в бокале будет огонь, а в груди — спокойствие.",
    "За тех, кто не играет по чужим правилам, а пишет свои.",
    "Чтобы страсть не выгорала, а разгоралась с каждым глотком.",
    "За тех, кто не коллекционирует людей, а ценит моменты.",
    "Чтобы каждый глоток был выбором, а не автоматизмом.",
    "За тех, кто не прячет характер за вежливостью.",
    "Чтобы в речи не было фальши, а в поступках — точности.",
    "За тех, кто не ждёт разрешения, чтобы быть собой.",
    "Пусть ночь будет долгой, а утро — без лишних оправданий.",
    "За тех, кто не боится быть неудобным, но остаётся верным себе.",
    "Пусть в словах будет пряность, а в делах — ясность.",
    "За тех, кто не коллекционирует лайки, а ценит взгляды.",
    "Чтобы страсть не выдыхалась, а разгоралась с каждым тостом.",
    "За тех, кто не ждёт разрешения, чтобы быть собой.",
    "Чтобы в жизни было больше огня и меньше воды.",
    "За тех, кто не играет в безопасные игры, а рискует красиво.",
    "Пусть каждый вечер будет экспериментом, а не обязанностью.",
    "За тех, кто не прячет свои желания за «потом».",
    "Чтобы каждый вечер оставлял историю, а не пустоту.",
    "За тех, кто не боится быть первым, кто скажет «хватит» или «ещё».",
    "Пусть в бокале будет не просто напиток, а настроение.",
    "За тех, кто не ждёт идеальных условий, а создаёт их здесь и сейчас.",
    "Выпьем за тех, кто не боится быть собой до конца. Пусть каждый тост будет не просто звуком бокалов, а эхом смелых решений. За вас!"
]

# ================= БАЗА ДАННЫХ =================
async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            count INTEGER DEFAULT 0,
            max_toasts INTEGER DEFAULT 10,
            total_toasts INTEGER DEFAULT 0,
            stopped_count INTEGER DEFAULT 0,
            continued_count INTEGER DEFAULT 0
        )''')
        await db.commit()

async def get_user(user_id: int) -> dict:
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
        if not row:
            new_limit = random.randint(7, 14)
            await db.execute("INSERT INTO users (user_id, max_toasts) VALUES (?, ?)", (user_id, new_limit))
            await db.commit()
            return {"user_id": user_id, "count": 0, "max_toasts": new_limit, "total_toasts": 0, "stopped_count": 0, "continued_count": 0}
        return dict(row)

async def update_user(user_id: int, **kwargs):
    if not kwargs: return
    fields = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values()) + [user_id]
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(f"UPDATE users SET {fields} WHERE user_id = ?", values)
        await db.commit()

# ================= ХЕНДЛЕРЫ =================
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍻 Выпить", callback_data="drink")]
    ])
    await message.answer("Сегодня отличный день, чтобы выпить 🌅\nМонетка решит, пора ли начинать.", reply_markup=kb)

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    u = await get_user(message.from_user.id)
    await message.answer(
        f"📊 Ваша статистика:\n"
        f"🍷 Всего тостов: {u['total_toasts']}\n"
        f"🛑 Остановлено вовремя: {u['stopped_count']}\n"
        f"🥂 Продолжено через «Нет»: {u['continued_count']}"
    )

@dp.callback_query(F.data == "drink")
async def cb_drink(callback: types.CallbackQuery):
    # 1️⃣ Анимация подбрасывания
    msg = await callback.message.answer("🪙 Подбрасываем монетку...")
    await asyncio.sleep(0.7)

    u = await get_user(callback.from_user.id)

    # 2️⃣ Проверка вероятности (70%)
    if random.random() < 0.7:
        toast = random.choice(TOASTS)
        progress = f"🍷 {u['count']} / {u['max_toasts']}"
        warning = "\n🥴 Вода уже скучает по тебе..." if u["count"] > 15 else ""

        show_choice = u["count"] >= u["max_toasts"]
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛑 Может хватит?", callback_data="maybe_stop"),
             InlineKeyboardButton(text="🥂 Все равно выпить", callback_data="keep_drinking")] if show_choice else
            [InlineKeyboardButton(text="🍻 Выпить", callback_data="drink")]
        ])
        await msg.edit_text(f"✅ Выпало: пить!\n{progress}\n🥂 {toast}{warning}", reply_markup=kb)
        await update_user(callback.from_user.id, count=u["count"] + 1, total_toasts=u["total_toasts"] + 1)
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🪙 Попробовать снова", callback_data="drink")]
        ])
        await msg.edit_text("❌ Монетка упала не той стороной...\nНе в этот раз. Повезёт в следующий клик!", reply_markup=kb)
        # Счётчик не меняется

@dp.callback_query(F.data == "maybe_stop")
async def cb_maybe_stop(callback: types.CallbackQuery):
    u = await get_user(callback.from_user.id)
    new_limit = random.randint(7, 14)
    await update_user(callback.from_user.id, count=0, max_toasts=new_limit, stopped_count=u["stopped_count"] + 1)
    await callback.answer("✅ Прогресс сброшен", show_alert=True)
    await cmd_start(callback.message)

@dp.callback_query(F.data == "keep_drinking")
async def cb_keep_drinking(callback: types.CallbackQuery):
    u = await get_user(callback.from_user.id)
    toast = random.choice(TOASTS)
    warning = "\n💧 Сделай глоток воды, прежде чем продолжить." if u["count"] > 20 else ""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛑 Может хватит?", callback_data="maybe_stop")],
        [InlineKeyboardButton(text="🥂 Все равно выпить", callback_data="keep_drinking")]
    ])
    await callback.message.answer(f"🍷 {u['count']} / {u['max_toasts']}\n🥂 {toast}{warning}", reply_markup=kb)
    await update_user(callback.from_user.id, count=u["count"] + 1, total_toasts=u["total_toasts"] + 1, continued_count=u["continued_count"] + 1)

# ================= HTTP СЕРВЕР ДЛЯ КРОНА =================
async def handle_ping(request):
    return web.Response(text="pong")

async def start_http_server(port: int):
    app = web.Application()
    app.router.add_get("/ping", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"✅ Keep-alive server on :{port}")

# ================= ЗАПУСК =================
async def main():
    await init_db()
    port = int(os.getenv("PORT", 8080))
    await start_http_server(port)
    logging.info("🚀 Bot polling started...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
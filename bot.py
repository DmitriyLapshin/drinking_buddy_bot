import os
import asyncio
import random
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("❌ Ошибка: Переменная BOT_TOKEN не найдена в окружении")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ================= 100 ТОСТОВ (4 КАТЕГОРИИ) =================
TOASTS_THEMES = {
    "philosophy": [
        "Выпьем за время, которое не ждёт, но учит.", "За тех, кто умеет слышать тишину между словами.",
        "Пусть путь будет важнее пункта назначения.", "За мудрость, которая приходит не с возрастом, а с принятием своих ошибок.",
        "Чтобы мы не теряли себя в поисках лучшего.", "За моменты, которые не фотографируют, а запоминают сердцем.",
        "Пусть сомнения будут не якорем, а компасом.", "За тех, кто не боится менять мнение, но не теряет принципы.",
        "Чтобы в жизни было больше «зачем» и меньше «почему».", "За истину, которая не кричит, а шепчет.",
        "Пусть каждый шаг осознан, даже если дорога неизвестна.", "За тех, кто не гонится за совершенством, а ценит подлинность.",
        "Чтобы память хранила свет, а не тени.", "За выбор, который делаем мы, а не обстоятельства.",
        "Пусть внутренний голос всегда будет громче внешнего шума.", "За тех, кто умеет отпускать, не ломая.",
        "Чтобы свобода была не отсутствием правил, а присутствием смысла.", "За дни, которые не просто проходят, а оставляют след.",
        "Пусть ошибки становятся ступенями, а не стенами.", "За тех, кто не путает занятость с важностью.",
        "Чтобы в сердце оставалось место для вопросов без ответов.", "За честность перед собой — она самая трудная.",
        "Пусть жизнь не будет черновиком, а сразу станет чистовиком.", "За тех, кто не требует гарантий, но верит в возможность.",
        "Выпьем за то, чтобы мы не забывали мечтать, даже когда научились считать."
    ],
    "cinema": [
        "За тех, кто в море, в поле и за этим столом!", "Пусть кони не спотыкаются, а друзья не подводят.",
        "За любовь, которая греет даже в самый лютый мороз.", "Чтобы крыша над головой не текла, а душа не черствела.",
        "За тех, кто пришёл вовремя — не на час, а на всю жизнь.", "Пусть удача ходит не гостьей, а соседкой по лестничной клетке.",
        "За мудрость, которая не учит, а напоминает.", "Чтобы в доме пахло хлебом, а не сплетнями.",
        "За тех, кто не бросает якорь, когда поднимается ветер.", "Пусть совесть будет чистой, а руки — тёплыми.",
        "За дружбу, которая не требует доказательств, но выдерживает проверку временем.", "Чтобы мечты не пылились на полке, а ждали на старте.",
        "За тех, кто умеет слушать, а не просто ждать своей очереди говорить.", "Пусть дождь моет улицы, а не настроение.",
        "За тех, кто не ищет лёгких путей, но находит верные.", "Чтобы в кармане звенело, а в сердце пелось.",
        "За людей, которые не боятся быть смешными, но остаются настоящими.", "Пусть наши слова будут легче воздуха, но крепче стали.",
        "За тех, кто пришёл, не постучав, но ушёл, оставив свет.", "Чтобы дорога была длинной, а привалы — радостными.",
        "За тех, кто не прячет слёзы, но умеет их вытирать.", "Пусть в жизни будет меньше «надо» и больше «хочу».",
        "За встречу, которая не требует слов, но оставляет след.", "Чтобы каждый тост был не просто звуком бокалов, а эхом добрых намерений.",
        "Выпьем за тех, кто не боится начать сначала, даже если уже написано полкниги."
    ],
    "short": [
        "За настоящее!", "Пусть будет легко.", "За тех, кто рядом.", "Чтобы всё сбылось.", "За чистые намерения.",
        "Пусть ветер будет попутным.", "За смелость быть собой.", "Чтобы не жалеть.", "За искренние слова.", "Пусть душа поёт.",
        "За тихую радость.", "Чтобы хватало сил.", "За верных друзей.", "Пусть не будет пустоты.", "За тёплый дом.",
        "Чтобы сердце не черствело.", "За ясный ум.", "Пусть удача любит.", "За простые вещи.", "Чтобы время не торопило.",
        "За добрые новости.", "Пусть не будет одиноко.", "За светлые головы.", "Чтобы хватило мудрости.", "За сегодняшний день!"
    ],
    "ironic": [
        "Выпьем за то, чтобы наши желания не отставали от зарплат!", "За тех, кто не считает калории, а считает счастливые моменты.",
        "Пусть холодильник никогда не пустеет, а кошелёк не худеет.", "За тех, кто не требует от нас идеальности, но ценит честность.",
        "Чтобы в телефоне всегда был интернет, а в жизни — связь.", "За мудрость, которая приходит после третьего, а не после сорока.",
        "Пусть проблемы решаются так же быстро, как заканчивается эта рюмка.", "За тех, кто не путает «занят» с «недоступен для важных людей».",
        "Чтобы утро было бодрым, а вечер — без последствий.", "За тех, кто не гонится за трендами, но всегда в форме.",
        "Пусть начальник хвалит, а зарплата приходит сама.", "За тех, кто умеет отдыхать, не чувствуя вины.",
        "Чтобы в жизни было больше «ой, повезло!» и меньше «опять я виноват».", "За тех, кто не прячет свои слабости, а использует их как преимущество.",
        "Пусть диета начинается завтра, а радость — сегодня.", "За тех, кто не требует от нас отчётов, но всегда рядом.",
        "Чтобы в голове было место для идей, а не для дедлайнов.", "За тех, кто не боится быть первым, кто скажет «хватит».",
        "Пусть выходные длятся дольше, а понедельник будет добрее.", "За тех, кто не путает громкость с аргументами.",
        "Чтобы в кармане всегда нашлось на такси, а в душе — на прощение.", "За тех, кто не требует от жизни гарантий, но создаёт уют.",
        "Пусть каждый тост будет коротким, а счастье — долгим.", "За тех, кто не гонится за количеством лайков, а ценит реальные встречи.",
        "Выпьем за то, чтобы завтра не пришлось жалеть о сегодняшнем!"
    ]
}

ALL_TOASTS = sum(TOASTS_THEMES.values(), [])

def get_toast(theme: str) -> str:
    pool = TOASTS_THEMES.get(theme, ALL_TOASTS) if theme != "all" else ALL_TOASTS
    return random.choice(pool)

# ================= СОСТОЯНИЕ (In-Memory) =================
users = {}

def get_user(uid: int) -> dict:
    if uid not in users:
        users[uid] = {"count": 0, "max_toasts": random.randint(7, 14), "theme": "all"}
    return users[uid]

# ================= ХЕНДЛЕРЫ =================
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    u = get_user(message.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍻 Выпить", callback_data="drink")],
        [InlineKeyboardButton(text="🎭 Темы", callback_data="themes")]
    ])
    await message.answer("Сегодня отличный день, чтобы выпить 🌅", reply_markup=kb)

@dp.callback_query(F.data == "themes")
async def cb_themes(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Все темы", callback_data="set_theme:all")],
        [InlineKeyboardButton(text="📖 Философские", callback_data="set_theme:philosophy")],
        [InlineKeyboardButton(text="🎬 Киношные", callback_data="set_theme:cinema")],
        [InlineKeyboardButton(text="⚡ Короткие", callback_data="set_theme:short")]
    ])
    await callback.message.edit_text("Выберите настроение:", reply_markup=kb)

@dp.callback_query(F.data.startswith("set_theme:"))
async def cb_set_theme(callback: types.CallbackQuery):
    theme = callback.data.split(":")[1]
    u = get_user(callback.from_user.id)
    u["theme"] = theme
    await callback.answer(f"Тема: {theme}", show_alert=True)
    await cmd_start(callback.message)

@dp.callback_query(F.data == "drink")
async def cb_drink(callback: types.CallbackQuery):
    u = get_user(callback.from_user.id)
    toast = get_toast(u["theme"])
    progress = f"🍷 {u['count']} / {u['max_toasts']}"
    warning = "\n🥴 Вода уже скучает по тебе..." if u["count"] > 15 else ""

    show_choice = u["count"] >= u["max_toasts"]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛑 Может хватит?", callback_data="maybe_stop"),
         InlineKeyboardButton(text="🥂 Все равно выпить", callback_data="keep_drinking")] if show_choice else
        [InlineKeyboardButton(text="🍻 Выпить", callback_data="drink")]
    ])
    await callback.message.answer(f"{progress}\n🥂 {toast}{warning}", reply_markup=kb)
    u["count"] += 1

@dp.callback_query(F.data == "maybe_stop")
async def cb_maybe_stop(callback: types.CallbackQuery):
    u = get_user(callback.from_user.id)
    u["count"] = 0
    u["max_toasts"] = random.randint(7, 14)
    await callback.answer("✅ Прогресс сброшен", show_alert=True)
    await cmd_start(callback.message)

@dp.callback_query(F.data == "keep_drinking")
async def cb_keep_drinking(callback: types.CallbackQuery):
    u = get_user(callback.from_user.id)
    toast = get_toast(u["theme"])
    warning = "\n💧 Сделай глоток воды, прежде чем продолжить." if u["count"] > 20 else ""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛑 Может хватит?", callback_data="maybe_stop")],
        [InlineKeyboardButton(text="🥂 Все равно выпить", callback_data="keep_drinking")]
    ])
    await callback.message.answer(f"🍷 {u['count']} / {u['max_toasts']}\n🥂 {toast}{warning}", reply_markup=kb)
    u["count"] += 1

# ================= HTTP СЕРВЕР ДЛЯ КРОНА =================
async def handle_ping(request):
    return web.Response(text="pong")

async def start_http_server(port: int):
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/ping", handle_ping)
    app.router.add_get("/health", handle_ping)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"✅ HTTP keep-alive server running on port {port}")

# ================= ЗАПУСК =================
async def main():
    port = int(os.getenv("PORT", 8080))
    await start_http_server(port)
    logging.info("🚀 Bot polling started...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
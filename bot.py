#!/usr/bin/env python3

import logging
# Отключаем **всё** логирование вплоть до уровня CRITICAL
logging.disable(logging.CRITICAL)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Раз вы отключили логи, можно просто получить пустой логгер
logger = logging.getLogger(__name__)

BOT_TOKEN = "7249869508:AAEdvohNBIOst-rMMG08-IgfPMOtKqQ6yqw"
CHANNEL_LINKS = {
    "lose_weight": "https://t.me/amyrskiu_parnisha",
    "gain_mass":   "https://t.me/amyrskiu_parnisha",
    "workout":     "https://t.me/amyrskiu_parnisha",
}

# === Обработчик /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text == "/start":
        user = update.effective_user
        # эти вызовы ничего не выведут, т.к. логирование отключено
        logger.info(f"/start от {user.full_name} (ID: {user.id})")

        welcome_text = (
            f"Привет, {user.first_name or 'друг'}!\n\n"
            "Я — твой спортивный помощник. Меня зовут Антон, "
            "я тренер с 10-летним опытом, работаю в полиции и люблю доски и мишкин&мишкин.\n\n"
            "Работаю со всеми уровнями подготовки. Давай разберёмся с твоими целями:"
        )

        keyboard = [
            [InlineKeyboardButton("💪 Похудение",         callback_data="lose_weight")],
            [InlineKeyboardButton("🏋️ Набор массы",      callback_data="gain_mass")],
            [InlineKeyboardButton("🤸 Обучение воркауту", callback_data="workout")],
        ]

        await update.message.reply_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# === Обработчик нажатий кнопок ===
async def handle_goal_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    goal = query.data
    link = CHANNEL_LINKS.get(goal)
    logger.info(f"Выбор цели '{goal}' от {user.full_name} (ID: {user.id})")

    if link:
        await query.edit_message_text(
            f"Отличный выбор! Получи материалы по ссылке 👇\n\n{link}"
        )
    else:
        logger.warning(f"Не найдена ссылка для цели '{goal}'")
        await query.edit_message_text("Произошла ошибка. Попробуй позже.")

# === Точка входа ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_goal_selection))

    logger.info("Бот запущен...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

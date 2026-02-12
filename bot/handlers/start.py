from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database.services.user_services import UserService

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user

    await UserService.get_or_create(
        telegram_id=tg_user.id,
        full_name=tg_user.full_name or "No name",
        language=tg_user.language_code or "uz"
    )

    await update.message.reply_text(
        "Xush kelibsiz! 👋\nBot muvaffaqiyatli ishga tushdi."
    )

start_handler = CommandHandler("start", start)

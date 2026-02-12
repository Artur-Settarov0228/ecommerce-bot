from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from config import settings

from database.services.user_services import UserService
from bot.keyboard.user_keyboards import main_menu
from bot.keyboard.admin_keyboards import admin_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await UserService.get_or_create(
        telegram_id=user.id,
        full_name=user.full_name or "No name",
        language=user.language_code or "uz"
    )

    # 🔐 AGAR ADMIN BO‘LSA
    if user.id in settings.ADMIN:
        await update.message.reply_text(
            "👑 Admin panel",
            reply_markup=admin_menu()
        )
    else:
        await update.message.reply_text(
            "Xush kelibsiz!",
            reply_markup=main_menu()
        )

start_handler = CommandHandler("start", start)

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Support:\n@your_support_username"
    )

support_handler = MessageHandler(
    filters.TEXT & filters.Regex("^📞 Support$"),
    support
)

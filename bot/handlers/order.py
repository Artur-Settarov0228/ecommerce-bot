from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

from bot.states.checkout_state import ASK_NAME, ASK_PHONE
from database.services.order_services import OrderService


# 🔹 1. Checkout boshlanishi
async def start_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✍️ Ismingizni kiriting:"
    )
    return ASK_NAME


# 🔹 2. Ismni olish
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await update.message.reply_text(
        "📞 Telefon raqamingizni yuboring:",
        reply_markup=keyboard,
    )
    return ASK_PHONE


# 🔹 3. Telefonni olish va order yaratish
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact:
        await update.message.reply_text("❌ Telefonni tugma orqali yuboring")
        return ASK_PHONE

    name = context.user_data["name"]
    phone = contact.phone_number
    user_id = update.effective_user.id

    order = await OrderService.checkout(
        user_id=user_id,
        name=name,
        phone=phone,
    )

    if not order:
        await update.message.reply_text("🛒 Savatcha bo‘sh")
        return ConversationHandler.END

    await update.message.reply_text(
        "✅ Buyurtma qabul qilindi!\n"
        "Tez orada siz bilan bog‘lanamiz."
    )

    return ConversationHandler.END


# 🔹 4. Cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Buyurtma bekor qilindi")
    return ConversationHandler.END


checkout_conversation = ConversationHandler(
    entry_points=[CommandHandler("checkout", start_checkout)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        ASK_PHONE: [MessageHandler(filters.CONTACT, get_phone)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

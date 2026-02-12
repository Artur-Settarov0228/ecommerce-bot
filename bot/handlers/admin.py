from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
)

from bot.states.product_state import ASK_NAME, ASK_PRICE, ASK_STOCK
from database.services.product_services import ProductService
from config import settings


# 🔐 admin tekshirish
def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN


# 1️⃣ boshlash
async def start_add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END

    await update.message.reply_text("📦 Mahsulot nomini kiriting:")
    return ASK_NAME


# 2️⃣ nom
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("💰 Narxini kiriting:")
    return ASK_PRICE


# 3️⃣ narx
async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text.isdigit():
        await update.message.reply_text("❌ Narx faqat raqam bo‘lsin")
        return ASK_PRICE

    context.user_data["price"] = int(update.message.text)
    await update.message.reply_text("📦 Qoldiq sonini kiriting:")
    return ASK_STOCK


# 4️⃣ qoldiq va saqlash
async def get_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text.isdigit():
        await update.message.reply_text("❌ Qoldiq faqat raqam bo‘lsin")
        return ASK_STOCK

    stock = int(update.message.text)

    await ProductService.create(
        name=context.user_data["name"],
        price=context.user_data["price"],
        stock=stock,
    )

    await update.message.reply_text("✅ Mahsulot qo‘shildi!")
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi")
    return ConversationHandler.END


add_product_conversation = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.TEXT & filters.Regex("^➕ Mahsulot qo‘shish$"),
            start_add_product,
        )
    ],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        ASK_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
        ASK_STOCK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_stock)],
    },
    fallbacks=[MessageHandler(filters.COMMAND, cancel)],
)

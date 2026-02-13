from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from database.session import SessionLocal
from database.models import Product
from sqlalchemy import select


# 1️⃣ Callback – mahsulotlarni ko‘rsatish
async def products_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with SessionLocal() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

    if not products:
        await update.message.reply_text("📦 Mahsulotlar yo‘q")
        return

    text = "🛍 Mahsulotlar:\n\n"
    for p in products:
        text += f"📦 {p.name}\n💰 {p.price} so‘m\n\n"

    await update.message.reply_text(text)


# 2️⃣ HANDLER — modul darajasida
products_handler = MessageHandler(
    filters.Regex("^🛍 Mahsulotlar$"),
    products_callback
)

from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from database.services.product_services import ProductService
from bot.keyboard.keyboards import product_keyboard


# /products komandasi
async def products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = await ProductService.get_all()

    if not products:
        await update.message.reply_text("Mahsulot yo‘q")
        return

    for p in products:
        await update.message.reply_text(
            f"📦 {p.name}\n💰 {p.price}",
            reply_markup=product_keyboard(p.id)
        )

products_handler = CommandHandler("products", products)


# 🛍 Mahsulotlar tugmasi
async def products_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await products(update, context)

products_text_handler = MessageHandler(
    filters.TEXT & filters.Regex("^🛍 Mahsulotlar$"),
    products_text
)

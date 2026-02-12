from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database.services.product_services import ProductService

async def products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = await ProductService.get_all()

    if not products:
        await update.message.reply_text("Mahsulot yo‘q")
        return

    text = ""
    for p in products:
        text += f"{p.name} — {p.price} so‘m\n"

    await update.message.reply_text(text)

products_handler = CommandHandler("products", products)

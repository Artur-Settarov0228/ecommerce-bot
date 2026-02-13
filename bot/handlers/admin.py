from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from database.session import SessionLocal
from database.models import Product


async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in [123456789]:
        await update.message.reply_text("❌ Ruxsat yo‘q")
        return

    try:
        name = context.args[0]
        price = int(context.args[1])
        description = " ".join(context.args[2:])
    except Exception:
        await update.message.reply_text(
            "❗ Format: /add_product nom narx tavsif"
        )
        return

    async with SessionLocal() as session:
        product = Product(name=name, price=price, description=description)
        session.add(product)
        await session.commit()

    await update.message.reply_text("✅ Mahsulot qo‘shildi")

async def products_text_callback(update, context):
    await products_callback(update, context)


    products_text_handler = MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        products_text_callback
    )
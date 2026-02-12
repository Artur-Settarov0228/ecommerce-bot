from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database.services.order_services import OrderService
from config import settings

async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    order = await OrderService.checkout(user_id)

    if not order:
        await update.message.reply_text("🛒 Savatcha bo‘sh")
        return

    # Userga javob
    await update.message.reply_text(
        f"✅ Buyurtma qabul qilindi!\n"
        f"🧾 Buyurtma ID: {order.id}\n"
        f"💰 Jami: {order.total_price}"
    )

    # Adminlarga xabar
    for admin_id in settings.ADMIN_IDS:
        await context.bot.send_message(
            chat_id=admin_id,
            text=(
                f"🆕 Yangi buyurtma!\n"
                f"🧾 ID: {order.id}\n"
                f"👤 User ID: {user_id}\n"
                f"💰 Jami: {order.total_price}"
            )
        )

checkout_handler = CommandHandler("checkout", checkout)

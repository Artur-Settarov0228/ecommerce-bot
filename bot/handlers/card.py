from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from database.services.card_services import CartService

# /cart — savatchani ko‘rish
async def view_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    items = await CartService.get_cart(user_id)

    if not items:
        await update.message.reply_text("🛒 Savatcha bo‘sh")
        return

    text = "🛒 Savatchangiz:\n\n"
    total = 0

    for item in items:
        price = item.product.price
        subtotal = price * item.quantity
        total += subtotal
        text += f"{item.product.name} x {item.quantity} = {subtotal}\n"

    text += f"\n💰 Jami: {total}"
    await update.message.reply_text(text)


# /add <product_id>
async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Product ID kiriting: /add 1")
        return

    product_id = int(context.args[0])
    user_id = update.effective_user.id

    await CartService.add(user_id, product_id)
    await update.message.reply_text("✅ Savatchaga qo‘shildi")


# /clear_cart
async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await CartService.clear(update.effective_user.id)
    await update.message.reply_text("🧹 Savatcha tozalandi")


cart_handler = CommandHandler("cart", view_cart)
add_handler = CommandHandler("add", add_to_cart)
clear_handler = CommandHandler("clear_cart", clear_cart)


async def add_from_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data  # add:1
    product_id = int(data.split(":")[1])
    user_id = query.from_user.id

    await CartService.add(user_id, product_id)
    await query.edit_message_reply_markup(None)
    await query.message.reply_text("✅ Savatchaga qo‘shildi")

add_button_handler = CallbackQueryHandler(add_from_button, pattern="^add:")

cart_text_handler = MessageHandler(
    filters.TEXT & filters.Regex("^🛒 Savatcha$"),
    view_cart
)
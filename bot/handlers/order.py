from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from bot.states.checkout_state import ASK_NAME, ASK_PHONE,ADDRESS
from database.session import SessionLocal
from database.models import User, Product, Order, OrderItem,card, card_item
from config import ADMIN
from sqlalchemy import select


# 🔹 checkout boshlanishi (inline tugmadan)
async def checkout_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "📱 Telefon raqamingizni kiriting:\nMasalan: +998901234567"
    )
    return ASK_PHONE


# 🔹 telefonni olish
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("📍 Yetkazib berish manzilini kiriting:")
    return ADDRESS


# 🔹 manzil → order yaratish
async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    phone = context.user_data["phone"]
    address = update.message.text

    with SessionLocal() as session:
        user = session.execute(
            select(User).where(User.telegram_id == telegram_id)
        ).scalar_one_or_none()

        if not user:
            await update.message.reply_text("❌ Foydalanuvchi topilmadi")
            return ConversationHandler.END

        cart = session.execute(
            select(card_item).where(card_item.user_id == user.id)
        ).scalar_one_or_none()

        if not cart:
            await update.message.reply_text("🛒 Savat bo‘sh")
            return ConversationHandler.END

        items = session.execute(
            select(card_item).where(card_item.cart_id == cart.id)
        ).scalars().all()

        if not items:
            await update.message.reply_text("🛒 Savat bo‘sh")
            return ConversationHandler.END

        total = 0
        products = {}

        for ci in items:
            product = session.get(Product, ci.product_id)

            if not product or not product.is_active:
                await update.message.reply_text("❌ Mahsulot mavjud emas")
                return ConversationHandler.END

            if product.stock < ci.quantity:
                await update.message.reply_text(
                    f"❌ {product.name} uchun qoldiq yetarli emas"
                )
                return ConversationHandler.END

            products[ci.product_id] = product
            total += product.price * ci.quantity

        # 🧾 ORDER
        order = Order(
            user_id=user.id,
            total_price=total,
            phone_number=phone,
            delivery_address=address,
            
        )
        session.add(order)
        session.flush()

        for ci in items:
            product = products[ci.product_id]

            session.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=ci.quantity,
                    price_snapshot=product.price,
                )
            )

            product.stock -= ci.quantity

        session.query(card_item).filter(
            card_item.cart_id == cart.id
        ).delete()

        session.commit()

    # 📩 ADMIN XABAR
    admin_text = f"""
🆕 YANGI BUYURTMA

📦 Order ID: #{order.id}

👤 {user.full_name}
🆔 {user.telegram_id}

📞 {phone}
📍 {address}

💰 {total:,} so'm
"""

    for product in products.values():
        admin_text += f"\n🛍 {product.name}"

    await context.bot.send_message(
        chat_id=ADMIN[0] if isinstance(ADMIN, list) else ADMIN,
        text=admin_text
    )

    await update.message.reply_text(
        "✅ Buyurtmangiz qabul qilindi!\nTez orada siz bilan bog‘lanamiz."
    )

    context.user_data.clear()
    return ConversationHandler.END


checkout_conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(checkout_start, pattern="^checkout$")
    ],
    states={
        ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
    },
    fallbacks=[],
)

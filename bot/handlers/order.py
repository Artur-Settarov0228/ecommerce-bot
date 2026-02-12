from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from bot.states.checkout_state import PHONE, ADDRESS
from database.session import SessionLocal
from database.models import User, Cart, CartItem, Product, Order, OrderItem, Status
from config import ADMIN
from sqlalchemy import select


# 🔹 checkout boshlanishi (inline tugmadan)
async def checkout_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "📱 Telefon raqamingizni kiriting:\nMasalan: +998901234567"
    )
    return PHONE


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
            select(Cart).where(Cart.user_id == user.id)
        ).scalar_one_or_none()

        if not cart:
            await update.message.reply_text("🛒 Savat bo‘sh")
            return ConversationHandler.END

        items = session.execute(
            select(CartItem).where(CartItem.cart_id == cart.id)
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
                return ConversationHandler.E

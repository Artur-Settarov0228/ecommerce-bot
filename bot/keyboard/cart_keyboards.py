from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def cart_actions():
    keyboard = [
        [
            InlineKeyboardButton("🧾 Buyurtma berish", callback_data="checkout")
        ],
        [
            InlineKeyboardButton("🧹 Tozalash", callback_data="clear_cart")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

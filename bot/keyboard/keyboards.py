from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back")]
    ])

def product_keyboard(product_id: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="➕ Savatchaga qo‘shish",
                callback_data=f"add:{product_id}"
            )
        ]
    ])
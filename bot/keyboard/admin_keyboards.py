from telegram import ReplyKeyboardMarkup

def admin_menu():
    keyboard = [
        ["➕ Mahsulot qo‘shish"],
        ["📦 Buyurtmalar"],
        ["⬅️ User menyu"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

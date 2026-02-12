from telegram import ReplyKeyboardMarkup

def main_menu():
    keyboard = [
        ["🛍 Mahsulotlar"],
        ["🛒 Savatcha"],
        ["📞 Support"]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

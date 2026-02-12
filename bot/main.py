from telegram.ext import Application
from config import settings

from bot.handlers.start import start_handler
from bot.handlers.product import products_handler
from bot.handlers.card import cart_handler, add_handler, clear_handler
from bot.handlers.order import checkout_handler

def main():
    app = Application.builder().token(settings.TOKEN).build()

    app.add_handler(start_handler)
    app.add_handler(products_handler)
    app.add_handler(add_handler)
    app.add_handler(cart_handler)
    app.add_handler(clear_handler)
    app.add_handler(checkout_handler)

    app.run_polling()

if __name__ == "__main__":
    main()

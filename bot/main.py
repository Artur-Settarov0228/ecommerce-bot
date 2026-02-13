from telegram.ext import Application, CommandHandler
from config import TOKEN

from bot.handlers.start import start_handler
from bot.handlers.product import products_handler, products_text_handler
from bot.handlers.card import (
    cart_handler,
    add_handler,
    clear_handler,
    add_button_handler,
    cart_text_handler,
)
from bot.handlers.support import support_handler
from bot.handlers.order import checkout_conversation
from bot.handlers.admin import add_product_conversation


def main():
    app = Application.builder().token(TOKEN).build()

    # ❗ ConversationHandler avval
    app.add_handler(add_product_conversation)
    app.add_handler(checkout_conversation)

    # Oddiy handlerlar
    app.add_handler(start_handler)
    app.add_handler(products_handler)
    app.add_handler(add_handler)
    app.add_handler(cart_handler)
    app.add_handler(clear_handler)
    app.add_handler(add_button_handler)
    app.add_handler(products_text_handler)
    app.add_handler(cart_text_handler)
    app.add_handler(support_handler)

    app.run_polling()


if __name__ == "__main__":
    main()

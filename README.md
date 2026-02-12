# ecommerce-bot


ecommerce_bot/
├── bot/                      # Telegram bot (faqat bot logika)
│   ├── __init__.py
│   ├── main.py               # Botni ishga tushirish
│   │
│   ├── handlers/             # Handlerlar
│   │   ├── __init__.py
│   │   ├── start.py          # /start, til tanlash
│   │   ├── product.py        # Mahsulotlarni ko‘rish
│   │   ├── cart.py           # Savatcha
│   │   ├── order.py          # Checkout
│   │   └── support.py        # Support / aloqa
│   │
│   └── keyboards.py          # Inline / Reply keyboardlar
│
├── database/                 # DATABASE (hammasi shu yerda)
│   ├── __init__.py
│   ├── connection.py         # Engine (PostgreSQL)
│   ├── session.py            # AsyncSession
│   │
│   └── models/               # MODELLAR
│       ├── __init__.py
│       ├── base.py
│       ├── user.py
│       ├── category.py
│       ├── product.py
│       ├── cart_item.py      # 🛒 CartItem
│       ├── order.py          # 📄 Order
│       └── order_item.py     # 📄 OrderItem
│
├── services/                 # BIZNES LOGIKA
│   ├── __init__.py
│   ├── user_service.py
│   ├── product_service.py
│   ├── cart_service.py
│   └── order_service.py
│
├── config.py                 # .env o‘qish
├── .env
├── requirements.txt
└── README.md

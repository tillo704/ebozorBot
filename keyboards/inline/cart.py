from loader import db
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


async def make_cart_items(cart_id):
    markup =InlineKeyboardMarkup(row_width=3)
    items = await db.select_user_cart_items(cart_id=cart_id)
    # for item in items:
    #     product_id = item["product_id"]
    #     products = await db.select_product(id=product_id)
    #     product = products[0]
        # markup.add(InlineKeyboardButton(text=))
    print(items)
    return markup
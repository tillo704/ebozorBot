from loader import db
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


async def make_cart_items(cart_id):
    total_price = 0    
    items = await db.select_user_cart_items(cart_id=cart_id)
    if items:
        message = "<b>Sizning savatingizdagi mahsulotlar</b> \n\n" 

        for item in items:
            markup =InlineKeyboardMarkup(row_width=3)
            quantity = item["quantity"]
            product_id = item["product_id"]
            products = await db.select_product(id=product_id)
            product = products[0]
            total_price += quantity * product['price']
            message += f"<b>{product['title']}({product['price']} $) x {quantity} = {product['price'] * quantity} $</b>\n"
            markup.add(InlineKeyboardButton(text="➖",callback_data=f"{product_id}_minus"),InlineKeyboardButton(text=f"🆑 {product['title']}",callback_data=f"{product_id}_delete"),(InlineKeyboardButton(text="➕",callback_data=f"{product_id}_plus")))
        markup.add(InlineKeyboardButton(text="Savatni bo'shtish",callback_data="clear_cart"))
    else:
        message = "Siznig savatingiz bo'sh "

    return markup , message , total_price
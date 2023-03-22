from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from data.config import ADMINS
from loader import db

def main_menu_markup(chat_id):
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)

    order = KeyboardButton(text="🛍 Buyurtma berish")
    my_order = KeyboardButton(text="📦 Buyurtmalarim")
    settings = KeyboardButton(text="⚙️ settings")


    main_menu.add(order)
    main_menu.add(my_order, settings)
    if chat_id in ADMINS :
        main_menu.add(KeyboardButton(text="🗂 Kategorya qo'shish!"),KeyboardButton(text="🗃 Mahsulot qo'shish!"))
    return main_menu

back = KeyboardButton(text= "⬅️ Orqaga")
menu = KeyboardButton(text= "🛖 Bosh menu")
cart = KeyboardButton(text="🛒 Savatcha ")
canfirm = KeyboardButton(text="📝 Rasmiylashtirish")



async def make_cats_markup():
    cats_markup = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    all_cats = await db.select_all_cats()
    for cat in all_cats:
        cats_markup.insert(KeyboardButton(text=cat["title"]))
    cats_markup.add(cart,canfirm)
    cats_markup.add(back,menu)
    return cats_markup




async def make_products_markup(cat_id):
    products_markup = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    all_products = await db.select_product(cat_id = cat_id)
    for product in all_products:
        products_markup.insert(KeyboardButton(text=product["title"]))
    products_markup.add(cart,canfirm)
    products_markup.add(back,menu)
    return products_markup


numbers = ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
for i in range(1,10):
    numbers.insert(KeyboardButton(text=str(i)))
numbers.add(cart,back)

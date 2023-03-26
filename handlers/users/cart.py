from aiogram import types
from loader import dp, db, bot
from keyboards.inline.cart import make_cart_items
from states.state_main import ShopState
from aiogram.dispatcher import FSMContext

dp.message_handler(text="🛒 Savatcha" , state="*")
async def get_cart_items(message: types.Message):
    user = await db.select_user(telegram_id = message.from_user.id)
    cart = await db.select_user_cart(user_id = user["id"])
    markup = await make_cart_items(cart_id=cart["id"])
    

    pass
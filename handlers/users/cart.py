from aiogram import types
from loader import dp, db, bot
from keyboards.inline.cart import make_cart_items
from keyboards.default.main import make_cats_markup
from aiogram.dispatcher import FSMContext

@dp.message_handler(text="🛒 Savatcha" , state="*")
async def get_cart_items(message: types.Message, state: FSMContext):
    user = await db.select_user(telegram_id = message.from_user.id)
    cart = await db.select_user_cart(user_id = user["id"])
    result = await make_cart_items(cart_id=cart["id"])
    # await message.answer(text=result[1],reply_markup=result[0])
    message = await message.answer(text=result[1],reply_markup=result[0])
    await state.update_data({"message": message, "total_price": result[2]}) 

@dp.callback_query_handler(text="clear_cart",state= "*")
async def clear_cart_items(call : types.CallbackQuery):
    user = await db.select_user(telegram_id = call.from_user.id)
    cart = await db.select_user_cart(user_id = user["id"])
    await db.clear_cart(cart_id=cart['id'])
    await call.answer("Savatingiz bo'shtildi ")
    await call.message.delete()
    markup = await make_cats_markup()
    await call.message.answer("Yana nimadir buyurtma qilasizmi?", reply_markup=markup)

@dp.callback_query_handler(state= "*")
async def update_cart_items(call : types.CallbackQuery):
    product_id, action = call.data.split("_")
    product_id = int(product_id )
    user = await db.select_user(telegram_id = call.from_user.id)
    cart = await db.select_user_cart(user_id = user["id"])
    chack_product = await db.select_cart_items(cart_id=cart["id"],product_id=product_id)
    if chack_product :
        quantity = chack_product["quantity"]
        if action == "plus":
            await db.update_cart_item(cart_id=cart["id"] , product_id=product_id , quantity=quantity + 1)
        elif action == "minus"  :
            await db.update_cart_item(cart_id=cart["id"] , product_id=product_id , quantity=quantity - 1)
        elif action == 'delete':
            await db.delete_cart_item(cart_id=cart["id"], product_id=product_id)         
    resualt = await make_cart_items(cart_id=cart["id"]) 
    await call.message.edit_text(text=resualt[1],reply_markup=resualt[0])  
    


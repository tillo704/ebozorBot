from aiogram import types
from loader import dp, db, bot
from states.state_main import ShopState
from keyboards.default.main import main_menu_markup,make_cats_markup,make_products_markup,menu
from aiogram.dispatcher import FSMContext

@dp.message_handler(text = "⬅️ Orqaga",state = ShopState.category)
async def get_menu(message :types.Message, state = FSMContext ):
    await message.answer("Asosiy menu",reply_markup=main_menu_markup(str(message.from_user.id)))
    await state.finish()



@dp.message_handler(text = "⬅️ Orqaga",state = ShopState.product)
async def get_menu(message :types.Message, state = FSMContext ):
    markup = await make_cats_markup()
    await message.answer("Nimadan boshlaymiz ?",reply_markup=markup)
    await ShopState.category.set()

@dp.message_handler(text = "⬅️ Orqaga",state = ShopState.quantity)
async def get_menu(message :types.Message, state = FSMContext ):
    data= await state.get_data()
    cat_id = data.get('cat_id')
    markup = await make_products_markup(cat_id=cat_id)
    await message.answer("Qaysi mahsulotni tanlaysiz?",reply_markup=markup)
    await ShopState.product.set()






@dp.message_handler(text = "🛖 Bosh menu",state = ShopState.category)
async def get_menu(message :types.Message, state = FSMContext ):
    await message.answer("Asosiy menu",reply_markup=main_menu_markup(str(message.from_user.id)))
    await state.finish()



@dp.message_handler(text = "🛖 Bosh menu",state = ShopState.product)
async def get_menu(message :types.Message, state = FSMContext ):
    await message.answer("Asosiy menu",reply_markup=main_menu_markup(str(message.from_user.id)))
    await state.finish()


@dp.message_handler(text = "🛖 Bosh menu",state = ShopState.quantity)
async def get_menu(message :types.Message, state = FSMContext ):
    await message.answer("Asosiy menu",reply_markup=main_menu_markup(str(message.from_user.id)))
    await state.finish()



@dp.message_handler(text = "⚙️ settings")
async def get_menu(message :types.Message):
    await message.answer("⚙️ bot sozlamalari uchin funksiya tuzilmagan.🥹",reply_markup=main_menu_markup(str(message.from_user.id)))
    
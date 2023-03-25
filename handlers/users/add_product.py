from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from states.admin import AddCategory,AddProduct
from keyboards.inline.main import make_cats_markup
from keyboards.default.main import main_menu_markup


@dp.message_handler(text="🗃 Mahsulot qo'shish!",user_id=ADMINS)
@dp.message_handler(commands=["add_product"],user_id=ADMINS)
async  def add_new_product_cmd(message: types.Message):
    markup = await make_cats_markup()
    await message.answer("Yangi qo'shmoqchi bo'lgan mahsulotingiz kategoriyasini tanlang !",reply_markup=markup)
    await AddProduct.cat.set()


@dp.callback_query_handler(state=AddProduct.cat,user_id = ADMINS)
async def get_product_id(call: types.CallbackQuery,state: FSMContext):
    cat = await db.select_category(title=call.data)
    cat_id = cat.get("id")
    await state.update_data({"cat_id": cat_id})
    await call.message.delete()
    await call.message.answer("Qo'shmoqchi bo'lgan maxsulotingiz nomini kiriting!")
    await AddProduct.title.set()


@dp.message_handler(user_id=ADMINS,state=AddProduct.title)
async def get_product_title(message: types.Message, state: FSMContext):
   praduct_title = message.text
   await state.update_data({"praduct_title": praduct_title})
   await message.answer("Maxsulot haqida batafsil ma'lumot kiriting!")
   await AddProduct.next()

@dp.message_handler(user_id=ADMINS,state=AddProduct.desc)
async def get_product_desc(message: types.Message, state: FSMContext):
   praduct_desc = message.text
   await state.update_data({"praduct_desc": praduct_desc})
   await message.answer("Maxsulot rasmini yuboring !")
   await AddProduct.next()

@dp.message_handler(content_types=["photo"],user_id=ADMINS,state=AddProduct.image)
async def get_product_image(message: types.Message, state: FSMContext):
   praduct_image = message.photo[-1].file_id
   await state.update_data({"praduct_image_id": praduct_image})
   await message.answer("Maxsulot narxini kiriting!")
   await AddProduct.next()


@dp.message_handler(lambda message: message.text.isdigit(),state=AddProduct.price)
async def get_price(message: types.Message, state=FSMContext):
   price = message.text
   data = await state.get_data()
   cat_id = data.get("cat_id")
   title = data.get("praduct_title")
   description = data.get("praduct_desc")
   image_id = data.get("praduct_image_id")
   # await db.add_praduct(title=title,description=description,image_url=image_id,price=price,cat_id=cat_id)
   await message.answer("Maxsulot saqlandi!",reply_markup=main_menu_markup(str(message.from_user.id)))
   await state.finish()
    
 
   
   
from aiogram import types
from loader import dp, db, bot
from keyboards.default.main import make_cats_markup , make_products_markup,numbers,main_menu_markup
from states.state_main import ShopState
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="🛍 Buyurtma berish")
async def get_cats_list(message : types.Message):
  markup = await make_cats_markup()
  await message.answer("Nimadan boshlaymiz 🤔 , Kategorya tanlang 👇",reply_markup=markup )
  await ShopState.category.set()


@dp.message_handler(state=ShopState.category)
async def get_cat(message: types.Message , state : FSMContext):
  cat_title = message.text
  cat = await db.select_category(title = cat_title)
  await state.update_data({"cat_id": cat["id"]})
  markup = await make_products_markup(cat_id=cat["id"])
  await message.answer_photo(photo=cat["image_url"],caption=cat["description"],reply_markup=markup)
  await ShopState.next()

@dp.message_handler(state= ShopState.product)
async def get_product(message: types.Message,state : FSMContext):
  product_title = message.text
  data= await state.get_data()
  cat_id = data.get('cat_id')
  products = await db.select_product(title=product_title,cat_id=cat_id)
  if products:
    product =products[0]
    msg = f"( <b>{product['title']}</b> \nNarxi: <i>{product['price']}</i>\n\n {product['description']})"
    await state.update_data({"prod_title":product['title'], 'prod_price':product['price']})
    await message.answer_photo(photo=product["image_url"],caption=msg,reply_markup=numbers)
    await ShopState.next()
  else:
    await message.answer("Mahsulot yo'q")





@dp.message_handler(state=ShopState.quantity)
async def get_quentity(message: types.Message , state: FSMContext):
  data = await state.get_data()
  title = data.get("prod_title")
  price = data.get("prod_price")
  msg = f"{title} ({price}$) x {message.text} = {int(message.text) * int(price)} "
  await message.answer(msg, reply_markup=main_menu_markup(str(message.from_user.id)))
  await state.finish()


  


# @dp.message_handler(state=ShopState.category)
# async def get_cat(message: types.Message):
#   cat_title = message.text
#   cat = await db.select_category(title = cat_title)
#   await message.answer_photo(photo=cat["image_url"],caption=cat["description"])
#   await ShopState.next()








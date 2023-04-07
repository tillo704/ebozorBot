from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

link_markup = InlineKeyboardMarkup()
link_markup.row(InlineKeyboardButton(text="Obuna !",url="@clay704"))



check_button =InlineKeyboardMarkup(    
    inline_keyboard=[[
             InlineKeyboardButton(text="✅ Obunani tekshirish ✅",callback_data="check_subs"),
            
            ]]
    )


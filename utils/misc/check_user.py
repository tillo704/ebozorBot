from data.config import CHANNELS
from .subscription import check
from aiogram import Bot

async def check_subs_user(user_id):
    final_status = True
    bot = Bot.get_current()
    result = str()
    for channel in CHANNELS:
        status =  await check(user_id=user_id, channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            final_status *= status
            result += f"✅ <b>{channel.title}</b> Kanallarga obuna bo'lgansiz...!\n "
        else:
            final_status *= False
            invite_link = await channel.export_invite_link()
            result += (f"❌ <a href='{invite_link}'><b>{channel.title}</b></a> kanalga obuna bo'lmagansiz") 

    return final_status,result



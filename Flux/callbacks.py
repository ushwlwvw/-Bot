import traceback
from Data import Data
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Flux.generate import generate_session

@Client.on_callback_query()
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    user = await bot.get_me()
    # user_id = callback_query.from_user.id
    mention = user["mention"]
    query = callback_query.data.lower()
    if query.startswith("home"):
        if query == 'home':
            chat_id = callback_query.from_user.id
            message_id = callback_query.message.message_id
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=Data.START.format(callback_query.from_user.mention, mention),
                reply_markup=InlineKeyboardMarkup(Data.buttons),
            )
    elif query == "about":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.ABOUT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif query == "help":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text = "** اليك كيفية الاستخدام** \ n"  +  البيانات . مساعدة ،
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif query == "انشاء":
        await callback_query.message.reply(
            "الرجاء اختيار مكتبة التي تريد إنشاء جلسة سلسلة عليها",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("بايروجرام", callback_data="بايروجرام"),
                InlineKeyboardButton("تيليثون", callback_data="تيليثون")
            ]])
        )
    elif query in ["بايروجرام", "تيليثون"]:
        await callback_query.answer()
        try:
            if query == "بايروجرام":
                await generate_session(bot, callback_query.message)
            else:
                await generate_session(bot, callback_query.message, telethon=True)
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            await callback_query.message.reply(ERROR_MESSAGE.format(str(e)))


ERROR_MESSAGE = "أُووبس! حدث استثناء! \n\n**خطأ** : {} " \
            "\n\nالرجاء زيارة  @H_M_Dr إذا كانت هذه الرسالة لا تحتوي على أي " \
            "معلومات حساسة وأنت إذا كنت تريد الإبلاغ عن هذا كـ " \
            ""

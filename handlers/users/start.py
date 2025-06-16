from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from pprint import pprint
import urllib.parse

from loader import dp, bot, db, db_admin
from utils.misc.subscription import check
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import REFERRAL_LINK
from keyboards.inline.subscription import check_subs
from keyboards.inline.send_link import share_link
from keyboards.inline.change_user_data import change_user_menu, confirm_changing
from keyboards.inline.channels_keyboard import channels_menu, check_sub
from utils.misc.subscription import check
from states.registration_state import PersonalData
from states.change_user_name_state import ChangeFullName
from keyboards.default.contactKeyboard import contact_keyboard
from keyboards.default.catalogForUsersKeyboard import for_users
from utils.misc.make_inline_kb import make_inline_kb
from utils.misc.t2html import text_to_html


@dp.message_handler(CommandStart(), chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message):
    CHANNEL = db_admin.get_channels_as_a_list()
    ADMINS = db_admin.get_adminstrators_as_list()

    print(CHANNEL)
    print(ADMINS)
    start_message = db_admin.get_message()[0]
    if start_message:
        print(f"start message: \n{start_message}")
        text = await text_to_html(start_message)
        text = urllib.parse.unquote(start_message)
        await message.answer(text=text, parse_mode=types.ParseMode.HTML)
    telegram_id = message.from_user.id
    channels_format = str()
    print(f"telegram_id: {telegram_id}")
    channels_format += "❗️Botdan toʻliq foydalanish uchun bizning Telegram sahifalarimizga obuna boʻling:\n"
    for channel in CHANNEL:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channels_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"
        button = InlineKeyboardButton(
            text=chat.title,
            url=invite_link
        )
        channels_menu.insert(button)

    text = f"Salom, {message.from_user.full_name}!\n"
    text += channels_format
    channels_menu.add(check_sub)
    await message.answer(text=text, reply_markup=channels_menu)
    channels_menu.inline_keyboard = []
    button = None
    
    if telegram_id in ADMINS:
        pass
    else:
        checking_invitation = message.get_args()
        invited_from = 0
        if checking_invitation:
            invited_from = int(checking_invitation.split('_')[-1])
        
        if message.from_user.id == invited_from:
            # agar foydalanuvchi o'zini referal havolasi orqali kirsa javob bermaslik
            await message.answer("Xush kelibsiz quyidagi tugmalar orqali botdan foydalaning", reply_markup=for_users)
            return
        
        count = db_admin.get_konkurs_count()
        print(count)
        db.add_user(telegram_id, invited_from=invited_from, konkurs_count=count)
        db.update_is_active(telegram_id, is_active=1)


@dp.callback_query_handler(text="check_subs",chat_type=types.ChatType.PRIVATE)
async def check_subscription(call: types.CallbackQuery):
    CHANNEL = db_admin.get_channels_as_a_list()
    
    await call.answer(cache_time=60)
    
    result = str()
    final_result = 1
    menu = InlineKeyboardMarkup()

    for channel in CHANNEL:
        status = await check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)
        
        if status:
            final_result *= 1
            result += f"<b>{channel.title}</b> kanaliga obuna bo‘lgansiz.\n\n"
        else:
            final_result *= 0
            invite_link = await channel.export_invite_link()
            result += (f"<b>{channel.title}</b> kanaliga obuna bo‘lmagansiz. ")

            button = InlineKeyboardButton(
                text=channel.title,
                url=invite_link
            )
            menu.add(button)
    menu.add(check_sub)
    
    if final_result:
        telegram_id = call.from_user.id
        check_user_in_db = db.check_full_registered(telegram_id)
        await call.message.delete()
        if check_user_in_db:
            await call.message.answer("Xush kelibsiz quyidagi tugmalar orqali botdan foydalaning", reply_markup=for_users)
            return
        await bot.send_message(call.from_user.id, "Hurmatli foydalanuvchi ism familiyangizni kiriting misol: Johongir Fozilov ")
        await PersonalData.fullname.set()
        return
    else:
        await call.message.answer(result, reply_markup=menu, disable_web_page_preview=True)
        menu.inline_keyboard = []

@dp.message_handler(state=PersonalData.fullname, chat_type=types.ChatType.PRIVATE)
async def get_full_name(message: types.Message, state: FSMContext):
    fullname = message.text
    if fullname in ["📊 Reyting", "💫 Jami ball", "Do'stlarni taklif qilish", "📞 Biz bilan aloqa", "🗂 Mening ma‘lumotlarim", "/start", "/help"]:
        await message.answer("Hurmatli foydalanuvchi siz ayni damda ismingizni kiritishingiz kerak")
        return
    if fullname:
        await state.update_data(
            {'fullname': fullname}
        )
        await message.answer("Hurmatli foydalanuvchi quyidagi tugmani bosish orqali telefon raqamingizni yuboring!", reply_markup=contact_keyboard)
        await PersonalData.phone_number.set()
        print(fullname)
    else:
        await message.answer("ism bo'sh bo'lishi mumkin emas")

@dp.message_handler(state=PersonalData.phone_number, content_types=types.ContentType.CONTACT, chat_type=types.ChatType.PRIVATE)
async def get_phone_number(message: types.Message, state: FSMContext):
    print(message.contact)
    if message.contact:
        phone_number = message.contact.phone_number
        await state.update_data(
            {'phone_number': phone_number}
        )
        data = await state.get_data()
        name = data.get('fullname')
        print(f'''
            ismingiz: {name},
            telefon raqamingiz: {phone_number}
        ''')
        db.update_user(
            telegram_id=message.from_user.id, 
            full_name=name,
            phone_number=phone_number,
            full_registered=True
        )

        invited_from = int(db.get_invited_from(message.from_user.id))
        if invited_from:
            people_invited = db.get_people_invited(invited_from)
            all_people_invited = db.get_all_people_invited(invited_from)
            people_invited = int(people_invited[0])
            all_people_invited = int(all_people_invited[0])
            
            people_invited += 1
            all_people_invited += 1
            db.update_user_people_invited(telegram_id=invited_from, people_invited=people_invited)            
            db.update_all_people_invited(telegram_id=invited_from, all_people_invited=all_people_invited)

        await state.reset_state(with_data=False)
        await message.answer("Xush kelibsiz quyidagi tugmalar orqali botdan foydalaning", reply_markup=for_users)
    else:
        await message.answer("Hurmatli foydalanuvchi kontaktni quyidagi tugmani bosish orqali yuboring", reply_markup=contact_keyboard)

@dp.message_handler(lambda message: db.check_user(message.from_user.id), text="Do'stlarni taklif qilish", chat_type=types.ChatType.PRIVATE)
async def get_referral_link(message: types.Message):
    referral_link = ''
    if db.check_user(message.from_user.id):
        referral_link = REFERRAL_LINK+str(message.from_user.id)
        print(referral_link)
    if referral_link:
        base_text = db_admin.get_message()[0]
        base_text = base_text.replace("@Kohinur_Academy_Konkursbot", referral_link)
        base_text = urllib.parse.quote(base_text)
        button = share_link.inline_keyboard.pop()[0]
        button.url = f"https://t.me/share/url?url={base_text}"
        share_link.add(button)
        text = "Quyidagi tugmani bosish orqali Botga do'stlaringizni taklif qiling va Konkursda yutish imkonyatingizni oshiring! 🎁\n👇👇👇👇"
        await message.answer(text, reply_markup=share_link)
    else:
        pass

@dp.message_handler(lambda message: db.check_user(message.from_user.id), text="📊 Reyting", chat_type=types.ChatType.PRIVATE)
async def get_rating(message: types.Message):
    num = 20
    index = 1
    result = db.get_rating()
    if len(result) < 20:
        num = len(result)
    main_text = f'''📊 Bu bo'lim orqali siz Umumiy Reyting bilan tanishishingiz mumkin:\nYuqori {num} lik\n'''    
    
    if len(result)>=21:
        result = result[:20]
    for user, rate in result:
        main_text += f"{index}. {user} - {rate}\n"
        index += 1
    await message.reply(main_text)

@dp.message_handler(lambda message: db.check_user(message.from_user.id), text="💫 Jami ball", chat_type=types.ChatType.PRIVATE)
async def get_rating(message: types.Message):
    number = db.get_people_invited(message.from_user.id)[0]
    if number:
        text = f"siz {number} ta odam taklif qilgansiz"
    else:
        text = "Siz hali hech kimni taklif qilmadingiz"
    await message.reply(text)

@dp.message_handler(lambda message: db.check_user(message.from_user.id), text="📞 Biz bilan aloqa", chat_type=types.ChatType.PRIVATE)
async def contact_us(message: types.Message):
    text = '''
        Konkurs haqidagi savolingiz va takliflaringiz boʻlsa murojaat qiling:
        @Shamshodxon_Odilov
        @Kohinur_Academy_Group
    '''
    await message.answer(text=text)

@dp.message_handler(lambda message: db.check_user(message.from_user.id), text="🗂 Mening ma‘lumotlarim", chat_type=types.ChatType.PRIVATE)
async def change_user_date(message: types.Message):
    await message.answer(text="Hurmatli foydalanuvchi agar ismingizni xato kiritgan bo'lsangiz uni o'zgartiring"\
                         "\nMarhamat ismingizni yozing. Misol uchun: Abduqodir Husanov", reply_markup=change_user_menu)
    await ChangeFullName.change_full_name.set()

@dp.callback_query_handler(state=ChangeFullName.change_full_name, chat_type=types.ChatType.PRIVATE)
async def reject_changin_name(call: types.CallbackQuery, state: FSMContext):
    if call.data == "deny_changing_user_name":
        await state.reset_state()
        await call.answer("Jarayon rad etildi")
    else:
        pass
    await call.message.delete()

@dp.message_handler(state=ChangeFullName.change_full_name, chat_type=types.ChatType.PRIVATE)
async def change_user_name(message: types.Message, state: FSMContext):
    name = message.text
    tg_id = message.from_user.id
    await message.answer(text=f"siz shu ismni yozdingiz: {name}\nIsmingizni to'g'ri yozganligingizga ishonchingiz komilmi?", reply_markup=confirm_changing)
    await state.update_data(
        {'name': name, 'tg_id': tg_id}
    )
    await ChangeFullName.confirm_changin_name.set()

@dp.callback_query_handler(state=ChangeFullName.confirm_changin_name, chat_type=types.ChatType.PRIVATE)
async def confirm_changinnn_username(call: types.CallbackQuery, state: FSMContext):
    print("blin")
    if call.data == "deny_changing_user_name":
        await call.message.delete()
        await call.answer("Jarayon rad etildi")
    if call.data == "confirm_changing_operate":
        data = await state.get_data()
        name = data.get('name')
        tg_id = data.get('tg_id')
        db.update_user_info(telegram_id=tg_id, fullname=name)
        await call.message.delete()
        await call.answer("Ismingiz muvaffaqiyatli saqlandi")
    elif call.data == "deny_changing_operate":
        await call.message.delete()
        await call.answer("Jarayon rad etildi")

    await state.reset_state()

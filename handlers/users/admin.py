import asyncio
from aiogram import types
from aiogram.types import ContentType, ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from sqlite3 import OperationalError

from loader import dp, db, db_admin
from loader import bot

from data.config import EXCEL_FILE, DEVELOPER_ID
from utils.misc.save_to_excel import convert_to_excel, save_to_excel
from keyboards.default.adminpanelKeyboard import admin_menu
from keyboards.inline.confirm_restart_competition import cofirm_menu
from keyboards.inline.confirm_advert import confirm_ad_menu
from keyboards.inline.change_start_message import ch_start_msg
from states.contact_developer import ContactDeveloper
from states.send_ad_state import Send_ad
from states.change_start_msg import ChangeStartMessage
from states.state_for_channel import ControlChannel
from keyboards.inline.deleting_channel_keyboard import make_channels_inline_for_admin


ADMINS = db_admin.get_adminstrators_as_list()

@dp.message_handler(CommandStart(), user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def start_admin(message: types.Message):
    await message.answer(text="Xush kelibsiz hurmatli Admin", reply_markup=admin_menu)


@dp.message_handler(Command('konkurs_xabari'), user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def change_comp_message(message: types.Message):
    await message.answer(
        "siz konkurs haqidagi xabarni yangilamoqchimisiz. Siz o'zgartirgan xabar barcha foydalanuvchilarga foydalanuvchi \start ni bosganda yuboriladi"\
        "marhamat start komandasi uchun chiqishi kerak bo'lgan xabarni kiriting",
    )
    await ChangeStartMessage.ch_msg.set()
    

@dp.message_handler(state=ChangeStartMessage.ch_msg, user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def confirm_change_start_msg(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(
        {
            "text": text
        }
    )
    await message.reply(
        "Siz foydalanuvchilar start ni bosganda shu xabar borishini tasdiqlaysizmi",
        reply_markup=ch_start_msg
    )


@dp.callback_query_handler(state=ChangeStartMessage.ch_msg, user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def saving_start_msg(call: types.CallbackQuery, state: FSMContext):
    text = await state.get_data()
    text = text.get('text')
    if call.data == "confirm_changing_start_message":
        db_admin.set_all_status_false()
        db_admin.add_message(text=text, status=True)
        await call.answer("Ma'lumot Saqlandi")
        await call.message.delete()
    elif call.data == "deny_changing_start_message":
        await call.answer("jarayon rad etildi")
        await call.message.delete()
    else:
        await call.answer("xatolik yuz berdi qaytadan urinib koring!")
        await call.message.delete()
    await state.reset_state()


@dp.message_handler(text="📊 Foydalanuvchilar soni", user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def send_users_to_admin(message: types.Message):
    konkurs = int(db_admin.get_konkurs_count())
    all_user = len(db.select_all_users(konkurs_count=konkurs))
    active_users = len(db.select_all_id(konkurs_count=konkurs))

    all_user2 = len(db.select_all_users())
    active_users2 = len(db.select_all_id())
    

    text = f"{konkurs} - konkurs natijalari:\nbotda {active_users} ta aktiv foydalanuvchi bor shulardan {all_user} tasi to'liq ro'yhatdan o'tgan\n"
    text += "-----------------\n"
    text += f"botning umumiy natijasi: \n{active_users2} ta aktiv\n{all_user2} ta to'liq ro'yhatdan o'tganlari bor"
    await message.answer(text=text)


@dp.message_handler(text="📈 Foydalanuvchilar reytingi", user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def send_users_to_admin(message: types.Message):
    main_text = '📊 Umumiy reyting (yuqori 20 lik):\n'
    index = 1
    result = db.get_rating()
    if len(result) >= 21:
        result = result[:20]
    for user, rate in result:
        main_text += f"{index}. {user} - {rate}\n"
        index += 1
        
    await message.reply(main_text)


@dp.message_handler(text="🗞 Reklama yuborish", user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def send_users_to_admin(message: types.Message):
    await message.answer(text="Marhamat yubormoqchi bo'lgan reklamangizni yuboring va u barcha foydalanuvchilarga yuboriladi:")
    await Send_ad.send_ad.set()


@dp.message_handler(state=Send_ad.send_ad, user_id=ADMINS, content_types=[ContentType.ANY], chat_type=types.ChatType.PRIVATE)
async def send_ad_to_users(message: types.Message, state: FSMContext):
    message_id = message.message_id
    await state.update_data(
        {'m_id': message_id}
    )
    text = 'Siz ushbu xabarni foydalanuvchilarga yubormoqchisiz, tasdiqlaysizmi?\n\n'
    await message.reply(text=text, reply_markup=confirm_ad_menu)


@dp.callback_query_handler(state=Send_ad.send_ad, user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def confirm_advert(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    m_id = data.get("m_id")
    if call.data == "yes_i_confirm_advert":
        from_chat_id = call.message.chat.id
        all_id = db.select_all_id()
        await call.message.delete()
        await call.answer(text=f"Reklama taxminan {len(all_id)*2 / 60}.2f daqiqada to'liq yuborib bo'linadi")
        for user in all_id:
            try:       
                await bot.copy_message(
                    chat_id=user[0],
                    from_chat_id=from_chat_id,
                    message_id=m_id
                )
            except Exception:
                db.update_is_active(user[0], 0)
            await asyncio.sleep(2)   
        await state.reset_state()       
        await call.message.answer("Xabaringiz jo'natildi!")

    elif call.data == "no_i_reject_advert":
        await state.reset_state()
        await call.answer("Jarayon rad etildi!")
        await call.message.delete()
    else:
        await call.answer("Xatolik yuz berdi!")
        await state.reset_state()
        await call.message.delete()


@dp.message_handler(text="📁 Yuklab olish", user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def send_users_to_admin(message: types.Message):
    all_users = db.select_all_users()
    all_users = convert_to_excel(all_users)
    await asyncio.sleep(2)
    save_to_excel(all_users)
    file = types.InputFile(path_or_bytesio=EXCEL_FILE)
    await message.answer_document(document=file,caption="foydalanuvchilarning barcha ma'lumotlari")


@dp.message_handler(text="restart_konkurs", user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def send_users_to_admin(message: types.Message):
    text = "Konkursni qayta boshlamoqchimisiz?"
    await message.answer(text, reply_markup=cofirm_menu)


@dp.callback_query_handler(user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def answer_call(call: types.CallbackQuery):
    if call.data == "yes_i_confirm":
        db.confimr_restart_competition()
        konkurs_count = db_admin.get_konkurs_count()
        konkurs_count += 1
        db_admin.update_konkurs(konkurs_count=konkurs_count)
        # await 
        await call.message.answer("Konkurs qayta boshlandi")
        
    elif call.data == "no_i_reject":
        await call.message.delete()
    else:
        pass
    
    await call.message.delete()
    await call.answer(text="Done!")


@dp.message_handler(text="☎️ Dasturchi bilan bog'lanish", user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def send_users_to_admin(message: types.Message):
    await message.answer(text="Marhamat Hurmatli Admin Dasturchiga savol yoki murojatingizni yo'llang")
    await ContactDeveloper.contact_developer.set()


@dp.message_handler(state=ContactDeveloper.contact_developer, content_types=[ContentType.ANY], chat_type=types.ChatType.PRIVATE)
async def contact_developer(message: types.Message, state: FSMContext):
    await bot.forward_message(
        chat_id=DEVELOPER_ID, 
        from_chat_id=message.chat.id, 
        message_id=message.message_id)
    await message.answer(text="xabaringiz Dasturchiga yuborildi! ")
    await state.reset_state()


@dp.message_handler(Command('add_channel'), user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def add_channel_handler(message: types.Message, state: FSMContext):
    await message.answer("kanalni kiriting \n misol: -> @Kohinur_Academy_Group \n Kanal maxfiy(private) bo'ladigan id ni olib yuboring \nmisol -> -1001820602074")

    await state.set_state(ControlChannel.add_channel)


@dp.message_handler(state=ControlChannel.add_channel, user_id=ADMINS, chat_type=types.ChatType.PRIVATE, content_types=[ContentType.ANY])
async def add_channel_to_db_handler(message: types.Message, state: FSMContext):
    channnel = message.text

    try:
        db_admin.add_channel(channel=channnel)
        await message.answer("Channel added to database successfully")
    except OperationalError:
        db_admin.create_channel_table()
        await message.answer("There's an error occured! Please try again")

    await state.reset_state()



@dp.message_handler(Command('delete_channel'), user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def add_channel_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "o'chirmoqchi bo'lgan kanalingiz ni tanlang", 
        reply_markup=make_channels_inline_for_admin())

    await state.set_state(ControlChannel.delete_channel)


@dp.callback_query_handler(state=ControlChannel.delete_channel, user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def deleting_channel_handler(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    _, channel_id = data.split('.')
    try:
        db_admin.delete_channel(channel_id=int(channel_id))
        await call.answer('Channel has been deleted succesfully')
    except OperationalError:
        await call.answer('Something went wrong try again or connect with developer')

    await call.message.delete()
    await state.reset_state()



@dp.message_handler(Command('add_admin'), user_id=ADMINS, chat_type=types.ChatType.PRIVATE)
async def add_admin_handler(message: types.Message, state: FSMContext):
    await message.answer('admin qo\'shish uchun uning telegram id sini yuboring masalan 2112312321')
    await state.set_state(ControlChannel.add_admin)


@dp.message_handler(state=ControlChannel.add_admin, user_id=ADMINS, chat_type=types.ChatType.PRIVATE, content_types=[ContentType.ANY])
async def add_admin_to_db_handler(message: types.Message, state: FSMContext):
    admin = message.text
    try:
        db_admin.add_admin(admin)
        await message.answer('New admin added to database successfully')
    except OperationalError:
        await message.answer('Something went wrong try again or connect with developer')
    
    await state.reset_state()

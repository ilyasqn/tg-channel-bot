import asyncio
import logging
import sys
import io
import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
# from aiogram.enums.content_type import ContentType
from aiogram.filters import Command
from datetime import timedelta

TOKEN = '6539135719:AAHewS3FDOiMoW_GcHvnioBcolnnZgFrE8g'
ADMIN_TELEGRAM_ID = '864278487'  # Замените на ваше реальное Telegram ID
CHANNEL_ID = '-1001940307290'
user_info = {}

bot = Bot(TOKEN)
dp = Dispatcher()

count = 0

def get_login_channel_kb() -> InlineKeyboardMarkup:
    channel_url = 'https://t.me/ilyas_qn'
    ikeyboard = [
        [InlineKeyboardButton(text='Вступить', url=channel_url)]
    ]
    ikb = InlineKeyboardMarkup(inline_keyboard=ikeyboard)
    return ikb




@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Добро пожаловать! Пожалуйста, отправьте фото вашего платежа.")


@dp.message(F.photo)
async def handle_payment_photo(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Без_имени"

    photo = message.photo[-1]  # Берем последний (наибольший) размер фотографии
    file_name = f'payment_photo_{user_id}.jpg'

    await bot.download(photo, file_name)

    await bot.send_photo(ADMIN_TELEGRAM_ID, FSInputFile(file_name),
                         caption=f"Платеж на подтверждение от user_id: {user_id}")

    await message.answer("Ваш чек получен и отправлен на подтверждение.")


@dp.message(Command('confirm'))
async def confirm_payment(message: Message):
    global count
    args = message.text.split()[1:]
    if args:
        user_id_to_confirm = args[0]
        if user_id_to_confirm.isdigit():
            # Получаем сохраненный username
            username = user_info.get(int(user_id_to_confirm), "Без_имени")

            # Рассчитываем дату истечения подписки
            expiration_date = datetime.datetime.now() + timedelta(days=30)
            expiration_date_str = expiration_date.strftime('%Y-%m-%d')

            # Записываем ID пользователя, его username и дату истечения подписки в файл
            with open('add.txt', 'a') as file:
                file.write(
                    f"{user_id_to_confirm} {username} {datetime.datetime.now().strftime('%Y-%m-%d')} {expiration_date_str}\n")

            await message.answer(f"Оплата пользователя с ID {user_id_to_confirm} ({username}) подтверждена.")

            await bot.send_message(chat_id=user_id_to_confirm, text="Ваша подписка активна на 30 дней.",
                                   reply_markup=get_login_channel_kb())
            count += 1
        else:
            await message.answer("Неверный ID пользователя. Пожалуйста, укажите корректный ID.")
    else:
        await message.answer("Пожалуйста, укажите ID пользователя после команды /confirm.")


def read_subscr(file):
    with open(file, 'r', encoding='utf-8', errors='replace') as file:
        lines = file.readlines()
        subsr_lst = [[line.split()[0], line.split()[-1]] for line in lines if len(line) >= 2]
        return subsr_lst


@dp.message(Command('check'))
async def send_end_subscr(message: Message):
    global count
    subscr_lst = read_subscr('add.txt')
    for lst in subscr_lst:
        today_day = datetime.datetime.now()
        subscr_end_date = datetime.datetime.strptime(lst[1], '%Y-%m-%d')
        if lst[1] == today_day.strftime('%Y-%m-%d'):
            await bot.ban_chat_member(CHANNEL_ID, int(lst[0]))
            await bot.unban_chat_member(CHANNEL_ID, int(lst[0]))
            count -= 1
        elif 0 < (today_day - subscr_end_date).days < 4:
            await bot.send_message(lst[0], 'Хотите продлить подписку?')
    
    cheaters_count = await bot.get_chat_member_count(CHANNEL_ID) - count
    await bot.send_message(ADMIN_TELEGRAM_ID, str(cheaters_count))
    result = await bot.get_chat_member(CHANNEL_ID, int(ADMIN_TELEGRAM_ID))
    await bot.send_message(ADMIN_TELEGRAM_ID, str(result))




async def main():
    await dp.start_polling(bot)
    await send_end_subscr()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
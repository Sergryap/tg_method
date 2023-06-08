import asyncio
import httpx

from environs import Env
from bot import Bot
from response_obj import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


async def main():
    """Примеры использования бота"""

    env = Env()
    env.read_env()
    token = env.str('TOKEN')
    chat_id = env.str('CHAT_ID')

    # Создание клавиатуры для Сообщение_1:
    button_1 = InlineKeyboardButton(text='button_1', callback_data='test')
    button_2 = InlineKeyboardButton(text='button_2', callback_data='test')
    button_3 = InlineKeyboardButton(text='button_3', callback_data='test')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_1, button_2, button_3],
            [button_2, button_3, button_1],
            [button_3, button_1, button_2]
        ]
    )

    # Создание клавиатуры для Сообщение_2:
    button_4 = KeyboardButton(text='button_4')
    button_5 = KeyboardButton(text='button_5')
    button_6 = KeyboardButton(text='button_6')
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [button_1, button_2, button_3],
            [button_2, button_3, button_1],
            [button_3, button_1, button_2]
        ],
        resize_keyboard=True
    )

    async with httpx.AsyncClient() as session:
        bot = Bot(token, session)
        await bot.send_message(chat_id, 'Сообщение_1', reply_markup=keyboard)
        await asyncio.sleep(2)
        await bot.send_message(chat_id, 'Сообщение_2', reply_markup=reply_keyboard)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

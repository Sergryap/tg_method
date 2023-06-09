import asyncio
import httpx
import tg_obj

from environs import Env
from bot import Bot
from pprint import pprint


async def main():
    """Примеры использования методов бота"""

    # Получаем необходимые переменные для бота: token и chat_id
    env = Env()
    env.read_env()
    token = env.str('TOKEN')
    chat_id = env.str('CHAT_ID')

    # Создание клавиатуры для Сообщение_1:
    button_1 = tg_obj.InlineKeyboardButton(text='button_1', callback_data='test')
    button_2 = tg_obj.InlineKeyboardButton(text='button_2', callback_data='test')
    button_3 = tg_obj.InlineKeyboardButton(text='button_3', callback_data='test')
    keyboard = tg_obj.InlineKeyboardMarkup(
        inline_keyboard=[
            [button_1, button_2, button_3],
            [button_2, button_3, button_1],
            [button_3, button_1, button_2]
        ]
    )

    # Создание клавиатуры для Сообщение_2:
    button_4 = tg_obj.KeyboardButton(text='button_4')
    button_5 = tg_obj.KeyboardButton(text='button_5')
    button_6 = tg_obj.KeyboardButton(text='button_6')
    reply_keyboard = tg_obj.ReplyKeyboardMarkup(
        keyboard=[
            [button_4, button_5, button_6],
            [button_5, button_6, button_4],
            [button_6, button_4, button_5]
        ],
        resize_keyboard=True
    )

    # Создаем session и делаем запросы для отправки сообщений:
    async with httpx.AsyncClient() as session:
        bot = Bot(token, session)
        res_1 = await bot.send_message(chat_id, 'Сообщение_1', reply_markup=keyboard)
        await asyncio.sleep(2)
        res_2 = await bot.send_message(chat_id, 'Сообщение_2', reply_markup=reply_keyboard)
        await asyncio.sleep(2)
        res_3 = await bot.send_photo(
            chat_id,
            'https://phonoteka.org/uploads/posts/2023-03/1679556522_phonoteka-org-p-opushka-lesa-foni-instagram-17.jpg',
            reply_markup=keyboard
        )
        pprint(res_1.dict())
        pprint(res_2.dict())
        pprint(res_3.dict())


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

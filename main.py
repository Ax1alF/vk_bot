import time
from datetime import datetime, date
from typing import Optional
from dotenv import load_dotenv
import os
import logging

import vk_api

load_dotenv()


TOKEN = os.getenv('VK_API_TOKEN')

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()


message = 'Это сообщение отправлено ботом\n Через enter'


def parse_vk_bdate(bdate_str: str) -> Optional[date]:
    """
    Парсит дату рождения из VK (форматы: 'dd.mm' или 'dd.mm.yyyy')
    Возвращает datetime.date или None, если формат некорректен
    """
    if bdate_str is None:
        return None

    try:
        parts = bdate_str.strip().split('.')
        if len(parts) == 3:
            day, month, year = map(int, parts)
            return date(year, month, day)
        elif len(parts) == 2:
            day, month = map(int, parts)
            return date(1900, month, day)
        else:
            return None
    except Exception:
        return None


def send_birthday_congrats():
    today = datetime.now()
    logging.info(f"Сегодня: {today.strftime('%d.%m')}")

    try:
        friends = vk.friends.get(fields='bdate,sex')['items']
    except Exception as e:
        logging.error(f'Ошибка получения друзей: {e}')
        return

    for friend in friends:
        bday = parse_vk_bdate(friend.get('bdate'))
        if bday is None:
            continue

        if bday.day == today.day and bday.month == today.month and friend['sex'] == 1:
            vk.messages.send(
                user_id=friend['id'],
                message=message,
                random_id=int(time.time() * 1000)
            )
            time.sleep(20)
            logging.info(f'Поздравление отправлено {friend["first_name"]} {friend["last_name"]}')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("log.log")
        ]
    )
    send_birthday_congrats()

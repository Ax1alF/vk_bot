import time
from datetime import datetime, date
from typing import Optional
from dotenv import load_dotenv
import os
import random
import logging

import vk_api
import textwrap

load_dotenv()


TOKEN = os.getenv('VK_API_TOKEN')

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

EXCLUDE_PEOPLE = [
    "Виктория Панченкова",
    "Светлана Киселева",
    "Татьяна Валентиновна",
    "Людмила Остапенко",
    "Виктория Панченкова",
    "Мария Прилипко",
    "Юлия Гиревая-Белоконева",
    "Инна Лавриненко",
    "Наталья Выпирайлова",
    "Оля Пахомова",
    "Лариса Косухина",
    "Марина Евстафьева",
    "Валентина Ноздрина",
    "Евгения Багатурия",
    "Анэлия Погорелова",
    "Алина Шерстюк",
    "Larisa Larisa",
    "Дарья Лебедева",
    "Дарья Ноздрина",
]


upload = vk_api.VkUpload(vk_session)
photo = upload.photo_messages('photo.jpg')[0]
attachment = f"photo{photo['owner_id']}_{photo['id']}"


def generate_message(name: str) -> str:
    return textwrap.dedent(f"""\
        {name}, Поздравляю с Днем рождения!
        Счастья, любви, много цветов и прекрасного настроения в этот замечательный день!
        💐🌺🌸🌹🌷💥🌟🎉💖🎀❤️💝🎂🍹🍺🍷🍸

        Для вас я дарю скидку 1000₽ на любую новую процедуру у нас в студии. Воспользоваться подарком можно в течение месяца.

        Чтобы забрать подарок, напишите мне в ответ «+»

        Топ мастер Школы-студии перманентного макияжа «ЭСТЕТИКА» Евгения Муравлёва

        https://vk.com/brovibelg_pm
    """)


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
            if f'{friend["first_name"]} {friend["last_name"]}' in EXCLUDE_PEOPLE:
                logging.info(f'Сегодня ДР у {friend["first_name"]} {friend["last_name"]}, не отправляем сообщение')
                continue

            vk.messages.send(
                user_id=friend['id'],
                message=generate_message(friend["first_name"]),
                random_id=int(time.time() * 1000),
                attachment=attachment
            )
            time.sleep(random.uniform(2.5, 5.0))
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
    # send_birthday_congrats()
    vk.messages.send(
        user_id=11830595,
        message=generate_message("Женя"),
        random_id=int(time.time() * 1000),
        attachment=attachment
    )



# id жени 11830595
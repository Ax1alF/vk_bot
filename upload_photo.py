import os
import random
import dotenv
import vk_api

dotenv.load_dotenv()

TOKEN = os.getenv('VK_API_TOKEN')
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

upload = vk_api.VkUpload(vk_session)
photo = upload.photo_messages('photo.jpg')[0]

attachment = f"photo{photo['owner_id']}_{photo['id']}"

# 3. Отправляем сообщение
USER_ID = 11830595  # <-- сюда ID получателя
vk.messages.send(
    user_id=USER_ID,
    message="Поздравляю с Днём рождения! 🎉",
    attachment=attachment,
    random_id=random.randint(0, 2**64)
)

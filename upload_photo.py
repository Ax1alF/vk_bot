import os

import dotenv
import vk_api

dotenv.load_dotenv()

TOKEN = os.getenv('VK_API_TOKEN')
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

upload = vk_api.VkUpload(vk_session)
photo = upload.photo_messages('photo.jpg')[0]

print(photo)
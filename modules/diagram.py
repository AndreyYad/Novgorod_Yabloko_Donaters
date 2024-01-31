from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from requests import post
from asyncio import run
from pprint import PrettyPrinter

from vk_bot.vk_bot import vk_session

async def create_diagram(collected: int, purpose: int):
    
    beautiful_num = lambda num: '{:,}'.format(num).replace(',', '\'')
    beautiful_collected = beautiful_num(collected)
    beautiful_purpose = beautiful_num(purpose)
    
    width = 500
    height = 100
    color = (255, 255, 255) 
    
    diagram = Image.new('RGB', (width, height), color)
    
    draw = ImageDraw.Draw(diagram)
    font = ImageFont.truetype('images/OceanwidePrimer-Semibold.otf', 36)
    draw.text((74, 25), f"{beautiful_collected}₽/{beautiful_purpose}₽", fill=(0, 0, 0), font=font)
    
    logo = Image.open('images/logo.png')
    diagram.paste(logo, (8, 20))
    
    dark_line = Image.open('images/dark_green_line.png')
    diagram.paste(dark_line, (74, 65))
    
    ratio = collected/purpose
    if ratio > 1:
        ratio = 1
    light_line = Image.open('images/light_green_line.png')
    light_line = light_line.crop((0, 0, light_line.size[0]*ratio, light_line.size[1]))
    diagram.paste(light_line, (74, 65))
    
    buffer = BytesIO()
    diagram.save(buffer, format='png')
    diagram_bytes = buffer.getvalue()
    
    return await get_vk_url(diagram_bytes)

async def get_vk_url(image_bytes: bytes):
    vk = vk_session.get_api()

    # Загрузка изображения в VK
    upload_url = vk.photos.getMessagesUploadServer()['upload_url']

    # Загрузка изображения на сервер VK
    files = {'photo': ('image.jpg', image_bytes)}
    response = post(upload_url, files=files).json()

    # Сохранение загруженного изображения
    photo = vk.photos.saveMessagesPhoto(
        server=response['server'],
        photo=response['photo'],
        hash=response['hash']
    )[0]

    # Получение URL загруженного изображения
    attachment = f"photo{photo['owner_id']}_{photo['id']}"
    
    msg_id = vk.messages.send(
        random_id=0,
        user_id=562027533,  
        message='',
        attachment=attachment
    )
    
    msg_data = vk.messages.getById(
        message_ids=msg_id
    )
    
    photo_url = msg_data['items'][0]['attachments'][0]['photo']['sizes'][-1]['url']
    
    return photo_url
    
if __name__ == '__main__':
    run(create_diagram(1000, 3000))
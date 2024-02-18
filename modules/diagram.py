from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from asyncio import run
from aiogram import types

async def get_size_font(collected: int, purpose: int):
    size = 52
    if 10000<=purpose<=99999 and collected>=10000:
        size = 49
    elif 100000<=purpose and len(str(collected))>3:
        match len(str(collected)):
            case 4:
                size -= 5
            case 5:
                size -= 8
            case 6:
                size -= 11
    return size

async def create_diagram(collected: int, purpose: int):
    
    beautiful_num = lambda num: '{:,}'.format(num).replace(',', '\'')
    beautiful_collected = beautiful_num(collected)
    beautiful_purpose = beautiful_num(purpose)
    
    width = 500
    height = 175
    color = (255, 255, 255) 
    size_font = await get_size_font(collected, purpose)
    
    diagram = Image.new('RGB', (width, height), color)
    
    draw = ImageDraw.Draw(diagram)
    font = ImageFont.truetype('images/OceanwidePrimer-Semibold.otf', size_font)
    draw.text((74, 44), f"{beautiful_collected}₽/{beautiful_purpose}₽", fill=(0, 0, 0), font=font)
    
    logo = Image.open('images/logo.png')
    diagram.paste(logo, (8, 60))
    
    dark_line = Image.open('images/light_green_line.png')
    diagram.paste(dark_line, (74, 114))
    
    ratio = collected/purpose
    if ratio > 1:
        ratio = 1
    light_line = Image.open('images/dark_green_line.png')
    light_line = light_line.crop((0, 0, light_line.size[0]*ratio, light_line.size[1]))
    diagram.paste(light_line, (74, 114))
    
    buffer = BytesIO()
    diagram.save(buffer, format='png')
    diagram_bytes = buffer.getvalue()
    
    return types.BufferedInputFile(diagram_bytes, filename='диаграма.png')
    
if __name__ == '__main__':
    run(create_diagram(1000, 3000))
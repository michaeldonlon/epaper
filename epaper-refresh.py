import time
import datetime
from PIL import Image,ImageDraw,ImageFont

# make sure the waveshare libs are on path, then import them
import sys
import os
picdir = os.path.join(os.getcwd(), 'pic')
libdir = os.path.join(os.getcwd(), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd2in13

font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)
font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)

try:
    epd = epd2in13.EPD()
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)

    # since the epaper started struggling to clear the screen, 
    # these images help to clear the screen properly
    image = Image.open(os.path.join(picdir, 'eraser_1.png'))
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    image = Image.open(os.path.join(picdir, 'eraser_2.png'))
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    epd.Clear(0xFF)

    # apply the qr code
    # new image - '1' for B&W image, dims, then 255 for white fill
    image = Image.new('1', (epd.height, epd.width), 255)
    im = Image.open(os.path.join(picdir, 'Chibud_2.4_qr.png'))
    image.paste(im, (3,3))

    today = datetime.date.today()
    date_display = today.strftime('%d/%m/%y')
    with open(f"./weatherdata/weather_{today.strftime('%Y-%m-%d')}.txt") as f:
        temp = f.read().splitlines()
        today_description = temp[0]
        today_max = temp[1]
        tomorrow_max = temp[2]
        f.close()
    tomorrow_day = (today + datetime.timedelta(days=1)).strftime('%A')

    # add the weather text and some borders
    draw = ImageDraw.Draw(image)
    draw.line([(125,90),(250,90)], fill=0, width=1)
    draw.line([(190,0),(190,18)], fill=0, width=1)
    draw.line([(190,18),(250,18)], fill=0, width=1)
    draw.text((131, 27), 'Today', font=font20, fill=0)
    draw.text((200, 28), f'{today_max}°C', font=font20, fill=0)
    draw.text((135, 100), f'{tomorrow_day}', font=font12, fill=0)
    draw.text((218, 101), f'{tomorrow_max}°C', font=font12, fill=0)
    draw.text((196, 2), f'{date_display}', font=font12, fill=0)
    if len(today_description) > 25 and '. ' in today_description:
        split_description = today_description.split('. ')
        draw.text((135, 60), f'{split_description[0]}.', font=font10, fill=0)
        draw.text((135, 72), f'{split_description[1]}', font=font10, fill=0)
    else:
        draw.text((135, 70), f'{today_description}', font=font10, fill=0)

    epd.display(epd.getbuffer(image))
    time.sleep(2)

    epd.sleep()

except:
    print('epaper failed')

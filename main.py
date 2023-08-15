import configparser
from telethon.sync import TelegramClient
import os

config = configparser.ConfigParser()
config.read("config.ini")
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']


async def download_videos(channel, catalog, temp_id):
    count_video = 0

    async for message in client.iter_messages(channel):
        if message.id <= temp_id or count_video == 100:
            break
        if message.video:
            path = await client.download_media(message.media, catalog + str(message.id))
            count_video += 1


def create_catalog(url):
    ind = url.find('t.me/')
    if not os.path.exists('Videos'):
        os.mkdir('Videos')
    catalog = 'Videos/' + url[ind + 5:]
    if not os.path.exists(catalog):
        os.mkdir(catalog)
        temp_id = 0
    else:
        s = os.listdir(catalog)
        temp_id = s[-1]
        ind = temp_id.find('.mp4')
        temp_id = temp_id[:ind]
    return catalog + '/', int(temp_id)


async def main():
    url = input("Введите ссылку на канал или чат: ")
    channel = await client.get_entity(url)
    catalog, temp_id = create_catalog(url)
    await download_videos(channel, catalog, temp_id)


with TelegramClient('anon', api_id, api_hash, system_version="4.16.30-vxdeal") as client:
    client.loop.run_until_complete(main())

import aiohttp
# import asyncio

from data import settings, BASE_DIR

URL = settings.zgy.url

async def schedule_downloader():
    """Функция, которая парсит расписание по чанкам с сайта згу"""

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(URL) as response:
            response.raise_for_status()

            with open(f"{BASE_DIR}{settings.schedule.path}{settings.schedule.file_name}", "wb") as f:
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)


# async def main():
#     await schedule_downloader()
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
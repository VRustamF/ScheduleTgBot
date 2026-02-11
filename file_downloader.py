import aiohttp
import asyncio

URL = 'https://norvuz.ru/upload/timetable/1-ochnoe.xls'

async def schedule_downloader():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(URL) as response:
            response.raise_for_status()

            with open("test.xls", "wb") as f:
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)


async def main():
    await schedule_downloader()


if __name__ == '__main__':
    asyncio.run(main())
import aiohttp
import asyncio
from src.hololive.hololive import get_live

async def main():
  for stream in await get_live():
    print(stream.start_scheduled)
    print("https://youtube.com/watch?v="+stream.id)

a = main()
asyncio.run(a)
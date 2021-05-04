from datetime import datetime, timedelta
from typing import List
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from asyncio.exceptions import TimeoutError

urls = ["https://hoololive-api.marnixah.com/schedule", "http://hololive-api2.marnixah.com/schedule"]

class Stream:
  title_jp: str
  talent_jp: str
  url: str
  starttime: datetime
  
async def get_streams() -> List[Stream]:
  streams: list[Stream] = []
  timeout = aiohttp.ClientTimeout(total=15)
  session = aiohttp.ClientSession()
  API_schedule = None
  for url in urls:
    try:
      API_schedule = await (await session.get(url, timeout=timeout)).json()
      break
    except ClientConnectorError:
      pass
    except TimeoutError:
      pass
  for day in API_schedule["schedule"]:
    date_month = day["date"].split("/")[0]
    date_day = day["date"].split("/")[1]
    for stream in day["schedules"]:
      stream_obj = Stream()
      stream_obj.url = str(stream["youtube_url"])
      stream_obj.title_jp = str(stream["title"])
      stream_obj.talent_jp = str(stream["member"])
      
      time_arr = stream["time"].split(":")
      hour = int(time_arr[0])
      minute = int(time_arr[1])

      current_time = datetime.utcnow()
      year = current_time.year

      stream_obj.starttime = datetime(
        year, int(date_month), int(date_day), hour, minute
      ) - timedelta(hours=9)  # JST is 9 hours ahead of UTC
      streams.append(stream_obj)
  await session.close()
  return streams
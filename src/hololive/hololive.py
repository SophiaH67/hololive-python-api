from datetime import datetime, timedelta
from typing import List
import json
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from asyncio.exceptions import TimeoutError

urls = ["https://hololive-api.marnixah.com/schedules", "http://hololive-api2.marnixah.com/schedules"]

class Stream:
  title_jp: str
  talent_jp: str
  url: str
  starttime: datetime
  
async def get_streams() -> List[Stream]:
  streams: list[Stream] = []
  session = aiohttp.ClientSession()
  API_schedule = None
  for url in urls:
    try:  
      API_schedule = json.loads(await (await session.get(url)).text())
      break
    except ClientConnectorError:
      pass
    except TimeoutError:
      pass
    except json.decoder.JSONDecodeError:
      pass
  await session.close()
  if API_schedule is None:
    return None
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
  return streams
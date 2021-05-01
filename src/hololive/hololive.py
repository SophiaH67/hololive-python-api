from datetime import datetime, timedelta
from typing import List
import requests

class Stream:
  title_jp: str
  talent_jp: str
  url: str
  starttime: datetime
  
async def get_streams() -> List[Stream]:
  streams: list[Stream] = []
  API_schedule = requests.get("https://hololive-api.marnixah.com/").json()
  for day in API_schedule["schedule"]:
    date_month = day["date"].split("/")[0]
    date_day = day["date"].split("/")[1]
    for stream in day["schedules"]:
      stream_obj = Stream()
      stream_obj.url = stream["youtube_url"]
      stream_obj.title_jp = stream["title"]
      stream_obj.talent_jp = stream["member"]
      
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
from datetime import datetime

class _API_stream:
  member: str
  time: str
  title: str
  youtube_url: str

class _API_day:
  date: str
  schedules: list[_API_stream]
  
class _API_schedule:
  region: str
  schedule: list[_API_day]

class Stream:
  title_jp: str
  title_romaji: str
  url: str
  starttime: datetime

class Hololive:
  streams: list[Stream]
  
  
  
from datetime import datetime
from typing import List, Optional
import aiohttp
from dateutil import parser
from enum import Enum
from os import getenv

url = getenv("HOLODEX_BASE_URL") or "https://holodex.net/api/v2"


class Status(Enum):
    NEW = "new"
    UPCOMING = "upcoming"
    LIVE = "live"
    PAST = "past"
    MISSING = "missing"


class Order(Enum):
    ASC = "asc"
    DESC = "desc"


class StreamType(Enum):
    STREAM = "stream"
    CLIP = "clip"


class Stream:
    id: str
    title: str
    type: StreamType
    topic_id: Optional[str]
    published_at: datetime
    available_at: datetime
    duration: int
    status: Status
    start_scheduled: Optional[datetime]
    start_actual: Optional[datetime]
    end_actual: Optional[datetime]
    live_viewers: Optional[int]
    description: Optional[str]
    songcount: Optional[int]
    channel_id: str
    channel_name: str
    channel_org: str
    channel_type: str
    channel_photo: str


async def get_live(channel_id: str = None, id: str = None, include: str = None, lang: str = None, limit: int = None, max_upcoming_hours: int = None, mentioned_channel_id: str = None, offset: int = None, order: Order = None, org: str = None, paginated: str = None, sort: str = None, status: Status = None, topic: str = None, type: StreamType = None) -> List[Stream]:
    """https://holodex.stoplight.io/docs/holodex/b3A6MTE2MjAyMzU-query-live-and-upcoming-videos

    Args:
        channel_id (str, optional): Filter by video uploader channel id. Defaults to None.
        id (str, optional): A single Youtube Video ID. If Specified, only this video can be returned (may be filtered out by other conditions though). Defaults to None.
        include (str, optional): Comma separated list of extra info for video. Defaults to None.
        lang (str, optional): A comma separated list of language codes to filter channels/clips, official streams do not follow this parameter. Defaults to None.
        limit (int, optional): Results limit. Defaults to None.
        max_upcoming_hours (int, optional): Number of maximum hours upcoming to get upcoming videos by (for rejecting waiting rooms that are two years out). Defaults to None.
        mentioned_channel_id (str, optional): Filter by mentioned channel id, excludes itself. Generally used to find collabs/clips that include the requested channel. Defaults to None.
        offset (int, optional): Offset results. Defaults to None.
        order (Order, optional): Order by ascending or descending. Defaults to None.
        org (str, optional): Filter by clips that feature the org's talent or videos posted by the org's talent. Defaults to None.
        paginated (str, optional): If paginated is set to any non-empty value, return an object with total, otherwise returns an array. Defaults to None.
        sort (str, optional): Sort by any returned video field. Defaults to None.
        status (Status, optional): Filter by video status. Defaults to None.
        topic (str, optional): Filter by video topic id. Defaults to None.
        type (Status, optional): Filter by video status. Defaults to None.


    Returns:
        List[Stream]: [description]
    """
    params = {
        "channel_id": channel_id,
        "id": id,
        "include": include,
        "lang": lang,
        "limit": limit,
        'max_upcoming_hours': max_upcoming_hours,
        "mentioned_channel_id": mentioned_channel_id,
        "offset": offset,
        "order": getattr(order, "value", None),
        "org": org,
        "paginated": paginated,
        "sort": sort,
        "status": getattr(status, "value", None),
        "topic": topic,
        "type": getattr(type, "value", None)
    }

    session = aiohttp.ClientSession()
    response = await (await session.get(url+"/live",
                                        # Remove None's from params
                                        params={
                                            k: v for k, v in params.items() if v is not None}
                                        )).json()

    streams: List[Stream] = []
    for res in response:
        stream = Stream()
        stream.id = res["id"]  # !
        stream.title = res["title"]  # !
        stream.type = StreamType.CLIP if res.get(
            "type", None) == "clip" else StreamType.STREAM
        stream.topic_id = res.get("topic_id", None)
        stream.published_at = parser.isoparse(res["published_at"])
        stream.available_at = parser.isoparse(res["available_at"])
        stream.duration = res["duration"]
        stream.status = res["status"]
        stream.start_scheduled = parser.isoparse(
            res["start_scheduled"]) if res.get("start_scheduled", None) else None
        stream.start_actual = parser.isoparse(
            res["start_actual"]) if res.get("start_actual", None) else None
        stream.end_actual = parser.isoparse(
            res["end_actual"]) if res.get("end_actual", None) else None
        stream.live_viewers = res.get("live_viewers", None)
        stream.description = res.get("description", None)
        stream.songcount = res.get("songcount", None)
        stream.channel_id = res["channel"]["id"]
        stream.channel_name = res["channel"]["name"]
        stream.channel_org = res["channel"]["org"]
        stream.channel_type = res["channel"]["type"]
        stream.channel_photo = res["channel"]["photo"]

        streams.append(stream)
    await session.close()
    return streams

# hololive-python-api

## Installation
```bash
pip install hololive
```

## Usage

```python
from hololive import hololive
streams = await hololive.get_streams()

for stream in streams:
  print(stream.title_romaji) # [Duolingo]? STADYYYYYYYYYYYY!!!!!!!!!# 2? [Momo Suzu Nene/Horo raibu]
  print(stream.title_jp) # 【Duolingo】🍑STADYYYYYYYYYYYY!!!!!!!!! #２🍑【桃鈴ねね/ ホロライブ】
  print(stream.talent_romaji) # Momo Suzu Nene
  print(stream.talent_jp) # 桃鈴ねね
  print(stream.starttime) # 2021-05-01 03:00:00
  print(stream.url) # https://www.youtube.com/watch?v=MWeu_kf2L94
  ```

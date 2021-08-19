# hololive-python-api

Gets stream info from holodex(no longer limited to only hololive)
## Installation
```bash
pip install hololive
```

## Usage

```python
from hololive import hololive
streams = await hololive.get_live(limit=5)

for stream in streams:
  print(stream.title)
# -----------------
# 【APEX】カスタム3日目【#あの伝WIN】
# 【APEX】 casual & arena rank?
# 【APEX】V最協決定戦カスタム4 #KGSWIN 【ぶいすぽ / 花芽すみれ】
# 【APEX】最協カスタム4日目→ソロランク修行【ふぇありす/弦月藤士郎/パカエル】
# 【Portal 2】 😈마왕적 포탈! 👾 魔王的ポータル😈 【NIJISANJI KR】
  ```

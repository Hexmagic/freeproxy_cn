Python3 免费的中国 http/https proxy 🚩


# Install

```
pip install freeproxy_cn
```

# Usage

获取免费代理，代理默认存在redis的db 0的`http`和`https`里，类型是list
```
from freeproxy_cn import Engin
import asyncio
asyncio.run(Enging().run())
```

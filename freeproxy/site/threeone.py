from freeproxy.core.channel import Channel
from freeproxy.util.pipe import to_doc


class ThreeOneF(Channel):
    def __init__(self):
        super(ThreeOneF, self).__init__()
        self.name = 'threeonef'
        self.td_idx = [2, 3]

    async def boostrap(self):
        content = await self.http.get('https://31f.cn/')
        doc = content >> to_doc
        self.funcmap = {
            self.handle: [
                'https://31f.cn' + ele for ele in doc.xpath('//table[position()=2]//a/@href')]
        }

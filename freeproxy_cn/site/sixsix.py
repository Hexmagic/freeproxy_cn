from typing import List, Tuple
from tqdm import tqdm
from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc

class Six(Channel):
    site_name = 'site'
    start_urls: list = [
        'http://www.66ip.cn/mo.php?sxb=&tqsl=200&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='
    ]  # 抓取的页面

    def __init__(self, debug=False, *arg, **kwargs):
        super(Six,self).__init__()

    async def run(self):
        '''
        抓取主函数
        '''        
        rst = []
        for url in tqdm(self.start_urls, desc=f"{self.site_name} grab"):
            proxies = await self.handle(url)
            rst += proxies
        return rst

    async def handle(self, url: str) -> List[Tuple[str, str]]:
        '''
        模板解析函数
        '''
        doc = await self.http_handler.get(self.session, url) >> to_doc
        items = doc.xpath("//body//text()")
        proxies = []
        for item in items:
            item = item.strip()
            lst = item.split(':')
            if len(lst) != 2:
                continue
            host, port = lst
            if len(port) > 5:
                continue
            proxies.append((host, port))        
        return proxies
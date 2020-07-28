from freeproxy_cn import Engin
import asyncio
from argparse import ArgumentParser
parser = ArgumentParser('Prxoy Crawl')
parser.add_argument('--valid_url', type=str, default='https://www.baidu.com')
parser.add_argument('--redis_host', type=str, default='localhost')
parser.add_argument('--redis_port', type=int, default=6379)
parser.add_argument('--redis_password', type=str, default='')
parser.add_argument('--valid_timeout',
                    type=int,
                    default=5,
                    help='验证代理请求指定url的timeout')
parser.add_argument('--redis_db', type=str, default=0, help='存储代理的redis数据库')
parser.add_argument('--valid_threads', type=int, default=4, help='验证使用的线程数')
parser.add_argument('--sleep_m', type=int, default=20, help='抓取间隔，默认20分组')
opt = parser.parse_args()
loop = asyncio.get_event_loop()

eng = Engin(redis_host=opt.redis_host,
            redis_port=opt.redis_port,
            redis_db=opt.redis_db,
            redis_password=opt.redis_password,
            valid_timeout=opt.valid_timeout,
            valid_threads=opt.valid_threads,
            valid_url=opt.valid_url)
eng.site_list()
loop.run_until_complete(asyncio.gather(eng.run()))

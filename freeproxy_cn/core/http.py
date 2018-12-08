from functools import wraps
from dummy_useragent import UserAgent
import aiohttp
from freeproxy_cn.util.pipe import extra_host


def wrap_http(func):
    @wraps(func)
    async def catch_exp(*args, **kwargs):
        slf = args[0]
        if slf.session.closed:
            slf.session = aiohttp.ClientSession(headers=slf.headers)
        # 捕获连接时和服务端拒绝连接的错误
        try:
            return await func(*args, **kwargs)
        except Exception:
            return ""

    return catch_exp


class Http(object):
    def __init__(self, session=None, timeout=30):
        self.headers = {"User-Agent": UserAgent().random()}
        self.timeout = timeout
        self.session = session
        self.proxy = None

    @wrap_http
    async def get(
        self,
        url,
        headers={},
        proxy=None,
        timeout=30,
        params=None,
        raw=False,
        binary=True,
        session=None,
    ):
        """
        session: reuse session
        url: support http or https
        headers:
        params: should be dict or tuple list or string
        proxy: only support http prefix such as http://127.0.0.1:1080
        timeout: default is 10
        raw: return res obj
        binary: return binary content ,default is False return text content
        """
        self.headers.update(headers)
        headers = self.headers
        headers["Host"] = url >> extra_host
        headers["User-Agent"] = UserAgent().random()
        session = session or self.session
        if session.closed:
            session = aiohttp.ClientSession()
        proxy = proxy or self.proxy
        async with session.get(
            url, headers=headers, proxy=proxy, timeout=timeout, params=params, ssl=False
        ) as res:
            if raw:
                return res
            else:
                if binary:
                    content = await res.read()
                else:
                    content = await res.text()
                if raw:
                    return res
                else:
                    return content

    @wrap_http
    async def post(
        self,
        url,
        session=None,
        headers={},
        proxy=None,
        timeout=30,
        data=None,
        json=None,
        raw=False,
        binary=True,
    ):
        """
        session: reuse session
        url: support http or https
        headers:
        params: should be dict or tuple list or string
        proxy: only support http prefix such as http://127.0.0.1:1080
        timeout: default is 10
        raw: return res obj
        binary: return binary content ,default is False return text content
        data: post dict or text
        json: dict
        """
        self.headers.update(headers)
        headers = self.headers
        session = session or self.session
        if session.closed:
            session = aiohttp.ClientSession()
        headers["Host"] = url >> extra_host
        headers["User-Agent"] = UserAgent().random()
        proxy = proxy or self.proxy
        async with session.post(
            url,
            headers=headers,
            data=data,
            json=json,
            proxy=proxy,
            timeout=timeout,
            ssl=False,
        ) as res:
            if binary:
                content = await res.read()
            else:
                content = await res.text()
            if raw:
                return res
            else:
                return content

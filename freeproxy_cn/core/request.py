import asyncio
import random
from concurrent.futures import TimeoutError
from copy import deepcopy
from typing import TypeVar, Union

import aiohttp
from aiohttp.web import Response
from dummy_useragent import UserAgent
from logzero import logger

__all__ = ("AsyncHttpHandler")

Session = Union[aiohttp.ClientSession]


def guard_200_status(response: Union[Response, Response]):
    return response.status == 200


class HttpHandler(object):
    def __init__(self, cache_path="cache", img_path="img", workers=10, *args, **kwargs):
        self.semp = asyncio.Semaphore(workers)
        self.last_url = ""

    def auto_handle_header(
        self, json: Union[str, None, dict], data: Union[str, None, dict], kwargs: dict
    ):
        """
        purpose: auto handle POST request header
        """
        headers = deepcopy(kwargs.get("headers", {}))
        # deepcopy 是为了不污染程序传入的headers
        if "User-Agent" not in headers:
            headers["User-Agent"] = UserAgent().random()
        if json:
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/json"
        if data:
            if "Content-Type" not in kwargs:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
        return headers

    async def get_response(self, session, url, param=None, raw=False, *args, **kwargs):
        pass

    def log_warning(self):
        pass

    async def get(self, session, url, params=None, *args, **kwargs):
        """
        method: str,
        session: Session,
        url: str,
        raw=False,
        params=None,
        json=None,
        data=None,
        timeout=30,
        filename=None,
        headers=None,
        with_status=False,
        check_func=None,
        """
        try:
            return await self.fetch(
                "GET", session, url=url, params=params, *args, **kwargs
            )
        except Exception:
            return

    async def post_response(self, session, url, data=None, json=None, raw=False, *args, **kwargs):
        pass

    async def post(self, session, url, data=None, json=None, *args, **kwargs):
        """
        method: str,
        session: Session,
        url: str,
        raw=False,
        params=None,
        json=None,
        data=None,
        timeout=30,
        headers=None,
        with_status=False,
        check_func=None,
        only_check_exists=False,
        """
        try:
            return await self.fetch(
                "POST", session, url=url, data=data, json=json, *args, **kwargs
            )
        except Exception:
            return

    async def fetch(
        self,
        method: str,
        session: Session,
        url: str,
        raw=False,
        params=None,
        json=None,
        data=None,
        timeout=30,
        headers=None,
        with_status=False,
        check_func=None,
        *args,
        **kwargs,
    ):
        with (await self.semp):
            if not headers:
                headers = self.auto_handle_header(json, data, kwargs)
            if raw:
                if method == "GET":
                    response = await self.get_response(
                        session,
                        url,
                        params=params,
                        timeout=timeout,
                        raw=True,
                        headers=headers,
                        **kwargs,
                    )
                    self.last_url = response.url
                else:
                    response = await self.post_response(
                        session,
                        url,
                        data=data,
                        json=json,
                        headers=headers,
                        timeout=timeout,
                        raw=True,
                        **kwargs,
                    )
                    self.last_url = response.url
                return response
            else:
                if method == "GET":
                    content, status = await self.get_response(
                        session,
                        url,
                        params=params,
                        timeout=timeout,
                        raw=False,
                        headers=headers,
                        **kwargs,
                    )

                else:
                    content, status = await self.post_response(
                        session,
                        url,
                        data=data,
                        json=json,
                        headers=headers,
                        timeout=timeout,
                        raw=False,
                        **kwargs,
                    )

                if with_status:
                    return content, status
                else:
                    return content


class AsyncHttpHandler(HttpHandler):
    def __init__(self, debug=False, worker=10, proxy=None, *args, **kwargs):
        super(AsyncHttpHandler, self).__init__(*args, **kwargs)

    async def get_response(self, session, url: str, params, timeout: int, headers: dict, raw: bool, **kwargs):
        async with session.get(
            url,
            params=params,
            timeout=timeout,
            headers=headers,
            verify_ssl=False,
            **kwargs,
        ) as response:
            self.last_url = response.url
            if raw:
                return response
            else:
                content = await response.read()
                return content, response.status

    async def post_response(
        self, session, url, data, json, timeout, headers, raw, **kwargs
    ):
        async with session.post(
            url,
            data=data,
            json=json,
            timeout=timeout,
            headers=headers,
            **kwargs,
        ) as response:
            self.last_url = response.url
            if raw:
                return response
            else:
                content = await response.read()
                return content, response.status

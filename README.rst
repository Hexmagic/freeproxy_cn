.. figure:: https://img.shields.io/pypi/pyversions/cuckoopy.svg
   :alt: 

免费的中国代理，网站列表

::

    [1]: lab.crossincode.com
    [2]: 89ip
    [3]: www.ip3366.net
    [4]: ip.jiangxianli.com
    [5]: www.kuaidaili.com
    [6]: www.xsdaili.com
    [7]: www.xicidaili.com
    [8]: www.superfastip.com
    [9]: www.freeip.top

安装
~~~~

::

    pip install freeproxy_cn

使用
~~~~

1. 循环抓取代理

.. code:: python

    >>> from freeproxy_cn import Engin
    >>> import asyncio
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(Engin().run())

2. 获取代理

   .. code:: python

       >>> from redis import Redis
       >>> rds = Redis()
       >>> rds.spop('http://icanhazip.com')
       192.168.1.1

参数说明
~~~~~~~~

\| Engin参数 \| 含义 \| \| -------------- \|
------------------------------------------------------------------------------------------------------------------------------
\| \| redis\_host \| 存储代理的redis的host \| \| redis\_port \|
存储代理的redis的port \| \| redis\_password \| 存储代理的redis的password
\| \| redis\_db \| 存储代理的redis使用哪个db,默认为0 \| \| valid\_thread
\| 用于验证代理有效性的线程数目，默认为4，想加快验证的可以适当增大该参数
\| \| valid\_per\_time \|
每批验证多少个代理地址，默认20个，可以适当增大该参数加快验证 \| \|
valid\_url \|
默认为一个返回请求IP\ `网站 <http://icanhazip.com>`__,这个网站没有区分http和https，\ **实际中需要换成自己要抓取的目标网站来验证代理**
\| \| valid\_timeout \| 验证超时时间设定，默认为5秒 \| ### 改进

可以使用一个web服务器代替redis进行代理提供，暂时还没有写

更新日期
~~~~~~~~

2019-12-23

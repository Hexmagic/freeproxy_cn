Introduce
############

.. image:: https://img.shields.io/pypi/v/cuckoopy.svg
    :target: https://pypi.python.org/pypi/cuckoopy

.. image:: https://img.shields.io/pypi/l/cuckoopy.svg
    :target: https://pypi.python.org/pypi/cuckoopy

.. image:: https://img.shields.io/pypi/wheel/cuckoopy.svg
    :target: https://pypi.python.org/pypi/cuckoopy

.. image:: https://img.shields.io/pypi/pyversions/cuckoopy.svg
    :target: https://pypi.python.org/pypi/cuckoopy

.. image:: https://travis-ci.org/rajathagasthya/cuckoopy.svg?branch=master
    :target: https://travis-ci.org/rajathagasthya/cuckoopy

免费http/https代理，抓取列表

+ https://www.cool-proxy.net
+ http://lab.crossincode.com
+ http://www.89ip.cn
+ https://proxy.l337.tech
+ http://www.ip3366.net
+ http://www.iphai.com
+ http://ip.jiangxianli.com
+ https://www.kuaidaili.com
+ https://www.proxydocker.com
+ http://ip.seofangfa.com
+ http://www.superfastip.com
+ https://31f.cn
+ http://www.xsdaili.com/
+ http://www.xicidaili.com
+ https://www.xroxy.com


Install
############

.. code-block::

    $ pip install freeproxy_cn


Usage
############

.. code-block:: python

    >>> from freeproxy_cn import Engin
    >>> import asyncio
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(Engin().run())

查看Redis的db0，可以看到http和https两个list

.. code-block:: python

    >>> from redis import Redis
    >>> rds = Redis()
    >>> rds.lpop('http')
    192.168.1.1

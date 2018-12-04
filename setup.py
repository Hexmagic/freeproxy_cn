import setuptools

setuptools.setup(
    name='freeproxy_cn',
    version='0.1',
    description='抓取免费的中国代理',
    long_description='',
    author='Hexmagic',
    packages=setuptools.find_packages(),
    include_package_data=True,
    author_email='191440042@qq.com',
    url='https://github.com/Hexmagic/freeproxy_cn.git',
    license='GNU General Public License v3.0',
    install_requires=['lxml', 'aiohttp', 'logzero',
                      'aredis', 'dummy_useragent', 'python-dateutil'],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ]
)

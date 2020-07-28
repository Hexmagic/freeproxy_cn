import setuptools

with open("README.rst",encoding='utf8') as f:
    long_description = f.read()

setuptools.setup(
    name="freeproxy_cn",
    version="1.6",
    description=long_description,
    long_description="",
    author="Hexmagic",
    packages=setuptools.find_packages(),
    include_package_data=True,
    author_email="191440042@qq.com",
    url="https://github.com/Hexmagic/freeproxy_cn.git",
    license="GNU General Public License v3.0",
    install_requires=[
        "lxml",
        "aiohttp",
        "logzero",
        "redis",
        "dummy_useragent",
        "python-dateutil",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
)

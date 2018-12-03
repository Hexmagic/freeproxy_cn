from datetime import datetime
from datetime import timedelta
import dateutil.parser
import time
from lxml import etree
import json
import functools
import urllib.parse


class pipe(object):
    def __init__(self, function):
        self.function = function
        self.rst = None
        functools.update_wrapper(self, function)

    def __rrshift__(self, other):
        return self.function(other)

    def __le__(self, other):
        if isinstance(other, pipe):
            self.rst = list(map(self.function, other.rst))
        else:
            self.rst = list(map(self.function, other))
        return self.rst

    def __call__(self, *args, **kwargs):
        return pipe(lambda x: self.function(x, *args, **kwargs))


@pipe
def to_dict(string):
    string = string or '{}'
    try:
        return json.loads(string)
    except Exception:
        return {}


@pipe
def to_doc(string):
    string = string or '<error></error>'
    return etree.HTML(string)


@pipe
def to_int(string):
    return int(string)


@pipe
def extra_head(doc, path=''):
    item = doc.xpath(path)
    if not item:
        return ''
    return item[0].strip('" \r\n\t')


@pipe
def extra_host(url):
    # 提取url中的Host
    return urllib.parse.urlparse(url).netloc


@pipe
def check(create_time):
    create_time = int(create_time)
    tody = datetime.now().date().isoformat()
    tody_timestamp = datetime.fromisoformat(tody).timestamp()
    if len(str(int(create_time))) == 13:
        if create_time >= tody_timestamp * 1000:
            return True
        return False
    else:
        if create_time >= tody_timestamp:
            return True
        return False


@pipe
def cst_to_timestamp(cst_str):
    tempTime = time.strptime(cst_str, '%a %b %d %H:%M:%S +0800 %Y')
    resTime = time.strftime('%Y-%m-%d %H:%M:%S', tempTime)
    rt = datetime.fromisoformat(resTime).timestamp()
    return rt * 1000


@pipe
def date_to_timestamp(date_str):
    date_str = date_str.split('-')
    if len(date_str[1]) == 1:
        date_str[1] = '0' + date_str[1]
    date_str = '-'.join(date_str)
    # linksfin 格式为’ 2018-8-09 12:12:12
    date_str = date_str.strip()
    return int(
        datetime.fromisoformat(
            date_str.replace("T", " ").replace(
                'Z', '').strip().split(".")[0].split('+')[0]).timestamp() *
        1000)


@pipe
def timestamp_to_date(stamp):
    return str(datetime.fromtimestamp(stamp / 1000))


@pipe
def get13timestamp(none):
    return int(time.time() * 1000)


@pipe
def gmt_to_timestamp(gmt):
    return int(
        (dateutil.parser.parse(gmt) + timedelta(hours=8)).timestamp() * 1000)

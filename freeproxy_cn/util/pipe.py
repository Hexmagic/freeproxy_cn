import functools
import json
from collections import defaultdict
from hashlib import md5
from itertools import cycle, takewhile
from typing import Dict, List, Union

try:
    from lxml import etree
except ImportError as e:
    lxml = None


class Monad(str):
    def __init__(self, data):
        self.data = data
        str.__init__(self)

    def __getitem__(self, attr):
        try:
            return Monad(self.data[attr])
        except Exception:
            return Monad("")

    def __repr__(self):
        if not self.data:
            return ""
        else:
            return self.data >> dumps_dict


def monad(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        rst = await func(*args, **kwargs)
        return Monad(rst)

    return inner


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
def to_list(obj):
    return list(obj)


@pipe
def xpath(doc, path=""):
    rst = []
    if isinstance(path, list):
        for ele in path:
            rst.append(doc.xpath(ele))
        return rst
    return doc.xpath(path)


@pipe
def to_str(obj):
    return str(obj)


@pipe
def mget(obj, keys=[], default=None):
    rst = []
    for key in keys:
        rst.append(obj.get(key, default))
    return rst


@pipe
def trim(data):
    return data.replace('"', "").replace("'", "").strip(" ").strip()


@pipe
def slice_by(lst, leng=3):
    return [lst[i: i + leng] for i in range(0, len(lst), leng)]


@pipe
def group_by_key(lst: List[Dict], key: str = "") -> Dict[str, List]:
    group:dict = defaultdict(list)
    for ele in lst:
        if isinstance(ele, dict):
            val = ele.get(key)
        else:
            val = getattr(ele, key)
        group[val].append(ele)
    return group


@pipe
def group_by_len(lst, leng=10):
    rst = []
    tmp = []
    for ele in lst:
        tmp.append(ele)
        if len(tmp) == leng:
            rst.append(tmp)
            tmp = []
    if tmp:
        rst.append(tmp)
    return rst


@pipe
def split_into_n(lst, leng=4):
    rst = []
    for x in range(leng):
        rst.append([])
    for x, y in zip(cycle(range(leng)), lst):
        rst[x].append(y)
    return rst


@pipe
def split_by(lst, sep=None):
    rst, tmp = [], []
    for ele in lst:
        if ele != sep:
            tmp.append(ele)
        else:
            rst.append(tmp)
            tmp = []
    if tmp:
        rst.append(tmp)
    return rst


@pipe
def head(lst: list, default=""):
    try:
        return lst[0]
    except Exception:
        return default


@pipe
def join(lst: list, sep="\t") -> str:
    return sep.join(list(map(str, lst)))


@pipe
def safe_int(string: str, default=1) -> int:
    try:
        return int(string)
    except Exception:
        return default


def dump(data: dict):
    return str(data)


@pipe
def simple_dumps(data: dict):
    return json.dumps(data, ensure_ascii=False)


@pipe
def dumps_dict(data: dict) -> str:
    tmp = json.dumps(data, ensure_ascii=False).replace("'", "")
    tj = json.loads(tmp)
    tmp = eval(str(tj).replace('"', ""))
    return json.dumps(tmp, ensure_ascii=False).replace("\\", "")


@pipe
def replace_lst_to(src: str, lstb: list, b="") -> str:
    for ele in lstb:
        src = src.replace(ele, b)
    return src


@pipe
def to_int(data):
    return int(data)


@pipe
def to_dict_safe(data):
    try:
        return json.loads(data)
    except:
        return {}


@pipe
def to_dict(data: Union[str, bytes], encoding="utf8") -> dict:
    # 替换字符中含有的双引号
    if isinstance(data, bytes):
        data = data.decode(encoding)
        try:
            return json.loads(data)
        except Exception:
            data = data.replace('\\"', "")
            return json.loads(data)
    else:
        try:
            return json.loads(data)
        except:
            # 单引号
            return eval(data)


@pipe
def to_xml(data):
    if isinstance(data, str):
        return etree.XML(data.encode("utf8"))
    else:
        return etree.XML(data)


@pipe
def to_doc(data: str):
    if isinstance(data, str):
        return etree.HTML(data)
    try:
        return etree.HTML(data.decode("utf8"))
    except:
        return etree.HTML(data)


@pipe
def strip_group(data, trim):
    while data.startswith(trim):
        data = data[len(trim):]
    while data.endswith(trim):
        data = data[: -len(trim)]
    return data


@pipe
def to_md5(data) -> int:
    if isinstance(data, list):
        data = "".join(data)
    md = md5()
    md.update(data.encode("utf8"))
    return str(md.hexdigest())


def main():
    lst = ["ac", "ac"] >= pipe(str.replace)("a", "c")
    print(lst)
    print("abcdefghij" >> slice_by(3))


if __name__ == "__main__":
    main()

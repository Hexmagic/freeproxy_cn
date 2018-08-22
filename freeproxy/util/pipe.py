import functools
import json
from lxml import etree


class pipe(object):
    # 类似unix的管道
    def __init__(self, function):
        self.function = function
        functools.update_wrapper(self, function)

    def __rrshift__(self, other):
        # 重写 >> 操作符
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return pipe(lambda x: self.function(x, *args, **kwargs))


@pipe
def to_str(obj):
    return str(obj)


@pipe
def to_int(obj):
    return int(obj)


@pipe
def to_dict(obj):
    return json.loads(obj)


@pipe
def to_doc(obj):
    return etree.HTML(obj)


@pipe
def extra_xpath(doc, xpath=None):
    return doc.xpath(xpath)


@pipe
def safe_extra(may_empty_lst):
    if may_empty_lst:
        return may_empty_lst[0].strip('"\t\n\r ').strip("'")
    else:
        return ''


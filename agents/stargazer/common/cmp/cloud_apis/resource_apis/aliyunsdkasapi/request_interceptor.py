# coding:utf-8

"""
Created on 2019-04-14

@author: junguo.kjg
"""


def url_decorator(fn):
    def decorator(*args, **kwargs):
        return "/asapi/v3" + fn(*args, **kwargs)

    return decorator


def get_query_params_decorator(fn):
    def decorator(*args, **kwargs):
        params = fn(*args, **kwargs)
        return params

    return decorator


def req_decor(cls):
    for attr_name in dir(cls):
        attr_value = getattr(cls, attr_name)
        if hasattr(attr_value, "__call__"):  # check if attr is a function
            # apply the function_decorator to your function
            # and replace the original one with your new one
            if attr_name == "get_url":
                setattr(cls, attr_name, url_decorator(attr_value))
            elif attr_name == "get_query_params":
                setattr(cls, attr_name, get_query_params_decorator(attr_value))
    return cls

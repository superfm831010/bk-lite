import datetime
import time

import pytz


def local_to_utc(local_time_str, local_tz="Asia/Shanghai", fmt="%Y-%m-%d %H:%M:%S", utc_fmt="%Y-%m-%dT%H:%M:%SZ"):
    local_time = datetime.datetime.strptime(local_time_str, fmt)

    # 将本地时间转换为UTC时间
    local_tz = pytz.timezone(local_tz)
    local_time = local_tz.localize(local_time)
    utc_time = local_time.astimezone(pytz.UTC)

    # 将UTC时间转换为字符串形式
    utc_time_str = utc_time.strftime(utc_fmt)

    return utc_time_str


def utc_to_local(utc_time_str, local_tz="Asia/Shanghai", fmt="%Y-%m-%d %H:%M:%S", utc_fmt="%Y-%m-%dT%H:%M:%SZ"):
    utc_time = datetime.datetime.strptime(utc_time_str, utc_fmt)

    # 将UTC时间转换为本地时间
    utc_time = pytz.UTC.localize(utc_time)
    local_time = utc_time.astimezone(pytz.timezone(local_tz))

    # 将本地时间转换为字符串形式
    local_time_str = local_time.strftime(fmt)

    return local_time_str


def dts_to_ts(dts_str, fmt="%Y-%m-%d %H:%M:%S"):
    """datetime把时间字符串转换为时间戳"""
    dts = datetime.datetime.strptime(dts_str, fmt)
    ts = int(time.mktime(dts.timetuple()))
    return ts


def utc_to_ts(utc_time_str, local_tz="Asia/Shanghai", fmt="%Y-%m-%d %H:%M:%S", utc_fmt="%Y-%m-%dT%H:%M:%SZ"):
    """UTC时间字符串转换为时间戳"""
    return dts_to_ts(utc_to_local(utc_time_str, local_tz, fmt, utc_fmt), fmt)

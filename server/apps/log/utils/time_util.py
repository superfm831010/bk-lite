from datetime import datetime, timedelta, timezone
import re


class TimeHelper:
    @staticmethod
    def get_time_range(range="5m"):
        # 当前 UTC 时间为 end
        end = datetime.now(timezone.utc)

        # 解析范围字符串（支持 "5m", "1h", "2d" 等）
        match = re.match(r"(\d+)([smhd])", range)
        if not match:
            raise ValueError(f"Invalid range format: {range}")

        value, unit = int(match.group(1)), match.group(2)
        if unit == "s":
            delta = timedelta(seconds=value)
        elif unit == "m":
            delta = timedelta(minutes=value)
        elif unit == "h":
            delta = timedelta(hours=value)
        elif unit == "d":
            delta = timedelta(days=value)
        else:
            raise ValueError(f"Unsupported time unit: {unit}")

        start = end - delta

        def format_time(dt):
            return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        return format_time(start), format_time(end)
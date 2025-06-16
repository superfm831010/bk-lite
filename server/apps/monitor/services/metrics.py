import pandas as pd

from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI


class Metrics:
    @staticmethod
    def get_metrics(query):
        """查询指标信息"""
        return VictoriaMetricsAPI().query(query)

    @staticmethod
    def get_metrics_range(query, start, end, step):
        """查询指标（范围）"""
        start = int(start)/1000  # Convert milliseconds to seconds
        end = int(end)/1000  # Convert milliseconds to seconds
        resp = VictoriaMetricsAPI().query_range(query, start, end, step)
        Metrics.fill_missing_points(start, end, step, resp.get("data", {}).get("result", []))
        return resp

    @staticmethod
    def fill_missing_points(start, end, step, data_list):
        """
        Fill missing time points in the `values` field for multiple instances using pandas frequency inference.
        :param start: Start timestamp in seconds (float)
        :param end: End timestamp in seconds (float)
        :param step: Time interval (seconds) (int)
        :param data_list: Data list, format [{"metric": dict, "values": [[timestamp, value], ...]}, ...]
        :return: Updated data list with missing points filled in `values`
        """
        for item in data_list:
            values = item["values"]

            if not values:
                continue

            # Convert original values to DataFrame
            original_df = pd.DataFrame(values, columns=["timestamp", "value"])
            original_df["timestamp"] = pd.to_datetime(original_df["timestamp"].astype(float), unit="s")
            original_df.set_index("timestamp", inplace=True)

            # Create complete time range DataFrame (start and end are now in seconds)
            full_time_index = pd.date_range(
                start=pd.to_datetime(start, unit="s"),
                end=pd.to_datetime(end, unit="s"),
                freq=f"{step}S"
            )
            full_df = pd.DataFrame(index=full_time_index, columns=["value"])
            full_df["value"] = None

            # Concatenate and sort all timestamps
            all_df = pd.concat([original_df, full_df])
            all_df = all_df[~all_df.index.duplicated(keep='first')]  # Keep original values for duplicates
            all_df.sort_index(inplace=True)

            # Convert back to the original `values` format
            result_values = []
            for ts, row in all_df.iterrows():
                timestamp_float = ts.timestamp()
                value = row["value"]
                # Convert NaN to None, keep original values
                if pd.isna(value):
                    value = None
                result_values.append([timestamp_float, value])

            item["values"] = result_values

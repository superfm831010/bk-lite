import os

import pandas as pd


class Utils:
    @staticmethod
    def save_data_to_csv(data_points, temp_dir: str, filename: str) -> str:
        """将数据点保存为CSV文件"""
        df = pd.DataFrame([point.dict() for point in data_points])
        file_path = os.path.join(temp_dir, filename)
        df.to_csv(file_path, index=False)
        return file_path

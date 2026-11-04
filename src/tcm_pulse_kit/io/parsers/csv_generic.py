"""通用CSV解析器.

解析通用CSV格式的脉搏数据。
"""

from typing import Dict, List, Optional
import numpy as np
import csv


class CSVGenericParser:
    """通用CSV解析器."""

    def __init__(self, fs: float = 1000.0):
        """初始化解析器.

        Args:
            fs: 采样率(Hz)
        """
        self.fs = fs

    def parse(self, filepath: str, column_map: Optional[Dict[str, int]] = None) -> Dict[str, np.ndarray]:
        """解析CSV文件.

        Args:
            filepath: 文件路径
            column_map: 列映射 {部位: 列索引}

        Returns:
            波形字典
        """
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    data.append([float(x) for x in row])
                except ValueError:
                    continue

        data = np.array(data)

        if column_map is None:
            # 默认映射
            column_map = {
                "左寸": 0,
                "左关": 1,
                "左尺": 2,
                "右寸": 3,
                "右关": 4,
                "右尺": 5,
            }

        result = {}
        for position, col_idx in column_map.items():
            if col_idx < data.shape[1]:
                result[position] = data[:, col_idx]

        return result

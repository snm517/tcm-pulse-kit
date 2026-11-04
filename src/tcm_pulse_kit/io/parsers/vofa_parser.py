"""VOFA+解析器.

解析VOFA+格式的脉搏数据。
"""

from typing import Dict
import numpy as np


class VofaParser:
    """VOFA+解析器."""

    def __init__(self, fs: float = 1000.0):
        """初始化解析器.

        Args:
            fs: 采样率(Hz)
        """
        self.fs = fs

    def parse(self, filepath: str) -> Dict[str, np.ndarray]:
        """解析VOFA+文件.

        Args:
            filepath: 文件路径

        Returns:
            波形字典
        """
        data = np.loadtxt(filepath, delimiter=',')

        # 默认6通道映射
        positions = ["左寸", "左关", "左尺", "右寸", "右关", "右尺"]
        result = {}

        for i, pos in enumerate(positions):
            if i < data.shape[1]:
                result[pos] = data[:, i]

        return result

"""数据尺度模块.

统一五行分析中的数据尺度。
"""

from typing import Dict
import numpy as np


class DataScaleUnifier:
    """数据尺度统一器.

    将不同来源的数据统一到相同尺度。
    """

    @staticmethod
    def unify_z_scores(z_scores: Dict[str, float]) -> Dict[str, float]:
        """统一z-score尺度.

        Args:
            z_scores: 原始z-score字典

        Returns:
            统一后的z-score字典
        """
        if not z_scores:
            return {}

        values = np.array(list(z_scores.values()))
        mean_val = np.mean(values)
        std_val = np.std(values) + 1e-10

        unified = {}
        for key, val in z_scores.items():
            unified[key] = float((val - mean_val) / std_val)

        return unified

    @staticmethod
    def normalize_to_range(
        values: Dict[str, float],
        target_range: tuple = (-1.0, 1.0),
    ) -> Dict[str, float]:
        """归一化到指定范围.

        Args:
            values: 原始值字典
            target_range: 目标范围

        Returns:
            归一化后的字典
        """
        if not values:
            return {}

        min_val = min(values.values())
        max_val = max(values.values())
        range_val = max_val - min_val + 1e-10

        target_min, target_max = target_range
        target_span = target_max - target_min

        normalized = {}
        for key, val in values.items():
            normalized[key] = target_min + (val - min_val) / range_val * target_span

        return normalized

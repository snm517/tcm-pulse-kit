"""相对值计算模块.

六部内部z-score标准化，Winsorization缩尾处理。
修复: A-008 winsorization替代完全排除。
"""

from typing import Dict, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class Fingerprint:
    """脉象指纹."""
    z_scores: Dict[str, float]
    fdr_values: Dict[str, float]


class RelativeEngine:
    """相对值引擎.

    对六部脉象特征进行内部z-score标准化。
    """

    EXTREME_VALUE_THRESHOLD = 3.0  # 缩尾阈值
    MAX_Z_SCORE = 3.0  # z-score上限
    MIN_STD = 1e-10  # 最小标准差

    def transform(self, raw_features: Dict[str, Dict]) -> Fingerprint:
        """转换为相对值指纹.

        Args:
            raw_features: 原始特征 {部位: {特征名: 值}}

        Returns:
            脉象指纹
        """
        if not raw_features:
            raise ValueError("无有效特征数据")

        if len(raw_features) < 2:
            raise ValueError("至少需要2个部位进行标准化")

        positions = list(raw_features.keys())

        z_scores = {}
        fdr_values = {}

        # 计算各特征的中位数和标准差
        for feature_name in ["peak_amp", "rise_ms", "fall_ms", "fwhm_ms", "area", "length"]:
            values = [raw_features[pos].get(feature_name, 0.0) for pos in positions]
            values = np.array(values, dtype=float)

            if len(values) == 0 or np.all(np.isnan(values)):
                continue

            # 使用Median Absolute Deviation计算稳健标准差
            med_val = np.median(values)
            mad = np.median(np.abs(values - med_val))
            robust_std = 1.4826 * mad + self.MIN_STD

            # Winsorization缩尾处理
            lower_bound = med_val - self.EXTREME_VALUE_THRESHOLD * robust_std
            upper_bound = med_val + self.EXTREME_VALUE_THRESHOLD * robust_std
            values = np.clip(values, lower_bound, upper_bound)

            # z-score标准化
            for i, pos in enumerate(positions):
                z = (values[i] - med_val) / robust_std
                z = np.clip(z, -self.MAX_Z_SCORE, self.MAX_Z_SCORE)

                if feature_name == "peak_amp":
                    z_scores[pos] = float(z)
                elif feature_name == "area":
                    fdr_values[pos] = float(z)

        # 计算浮沉比标准化
        if z_scores and fdr_values:
            for pos in positions:
                if pos in z_scores and pos in fdr_values:
                    fdr_values[pos] = z_scores[pos] - fdr_values[pos]

        return Fingerprint(z_scores=z_scores, fdr_values=fdr_values)

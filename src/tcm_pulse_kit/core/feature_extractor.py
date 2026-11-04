"""特征提取模块.

从单个脉搏周期提取特征。
修复: A-012 增加cv_peak_amp和cycle_correlation。
"""

from dataclasses import dataclass, asdict
from typing import Dict
import numpy as np
from scipy import signal


@dataclass
class CycleFeatures:
    """周期特征."""
    peak_amp: float
    rise_ms: float
    fall_ms: float
    fwhm_ms: float
    area: float
    length: float
    cv_peak_amp: float = 0.0
    cycle_correlation: float = 0.0

    def to_dict(self) -> Dict:
        return asdict(self)


class CycleFeatureExtractor:
    """周期特征提取器.

    从单个脉搏周期提取多维特征。
    """

    def __init__(self, fs: float = 1000.0):
        """初始化提取器.

        Args:
            fs: 采样率(Hz)
        """
        self.fs = fs

    def extract(self, cycle: np.ndarray) -> CycleFeatures:
        """提取周期特征.

        Args:
            cycle: 单个周期波形

        Returns:
            周期特征
        """
        # 峰值幅度
        peak_idx = np.argmax(cycle)
        peak_amp = float(cycle[peak_idx])

        # 上升时间
        rise_ms = peak_idx / self.fs * 1000.0

        # 下降时间
        fall_ms = (len(cycle) - peak_idx) / self.fs * 1000.0

        # FWHM
        half_max = peak_amp / 2.0
        above_half = np.where(cycle >= half_max)[0]
        fwhm_ms = (above_half[-1] - above_half[0]) / self.fs * 1000.0 if len(above_half) > 1 else 0.0

        # 面积 (有符号面积)
        area = float(np.trapz(cycle, dx=1.0/self.fs))

        # 脉长
        length = len(cycle) / self.fs * 1000.0

        # 变异系数
        cv_peak_amp = float(np.std(cycle) / (np.mean(np.abs(cycle)) + 1e-10))

        # 周期相关性 (与正弦模板的相关性)
        template = np.sin(np.linspace(0, np.pi, len(cycle)))
        cycle_correlation = float(np.corrcoef(cycle, template)[0, 1]) if len(cycle) > 1 else 0.0

        return CycleFeatures(
            peak_amp=peak_amp,
            rise_ms=rise_ms,
            fall_ms=fall_ms,
            fwhm_ms=fwhm_ms,
            area=area,
            length=length,
            cv_peak_amp=cv_peak_amp,
            cycle_correlation=cycle_correlation,
        )

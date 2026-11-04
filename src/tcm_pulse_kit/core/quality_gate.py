"""质量门禁模块.

评估数据质量和诊断可信度。
修复: A-013 增加低频噪声和谱平坦度。
"""

from typing import Dict, List
from dataclasses import dataclass
import numpy as np
from scipy import signal


@dataclass
class QualityResult:
    """质量评估结果."""
    overall_confidence: float
    flags: List[str]


class QualityGate:
    """质量门禁.

    评估脉搏数据质量和诊断可信度。
    """

    SNR_THRESHOLD = 10.0
    SPECTRAL_FLATNESS_THRESHOLD = 0.3
    LOW_FREQ_NOISE_THRESHOLD = 0.1

    def evaluate(self, features_by_pos: Dict[str, List[Dict]]) -> QualityResult:
        """评估数据质量.

        Args:
            features_by_pos: 各部位特征列表

        Returns:
            质量评估结果
        """
        flags = []
        total_confidence = 1.0

        for position, features in features_by_pos.items():
            if not features:
                flags.append(f"{position}: 无有效特征")
                total_confidence *= 0.5
                continue

            # 连续性检查
            peak_amps = [f.get("peak_amp", 0.0) for f in features]
            if len(peak_amps) < 2:
                flags.append(f"{position}: 周期数不足")
                total_confidence *= 0.7
                continue

            # 标准差检查
            std_val = np.std(peak_amps)
            if std_val > np.mean(peak_amps) * 0.3:
                flags.append(f"{position}: 周期一致性差")
                total_confidence *= 0.8

            # SNR评估
            snr = self._calculate_snr(peak_amps)
            if snr < self.SNR_THRESHOLD:
                flags.append(f"{position}: SNR低 ({snr:.1f}dB)")
                total_confidence *= 0.85

            # 谱平坦度检查
            flatness = self._calculate_spectral_flatness(peak_amps)
            if flatness > self.SPECTRAL_FLATNESS_THRESHOLD:
                flags.append(f"{position}: 谱平坦度高 ({flatness:.2f})")
                total_confidence *= 0.9

            # 低频噪声检查
            low_freq_noise = self._calculate_low_freq_noise(peak_amps)
            if low_freq_noise > self.LOW_FREQ_NOISE_THRESHOLD:
                flags.append(f"{position}: 低频噪声高 ({low_freq_noise:.2f})")
                total_confidence *= 0.9

        if not flags:
            flags.append("数据质量良好")

        return QualityResult(
            overall_confidence=total_confidence,
            flags=flags,
        )

    def _calculate_snr(self, values: List[float]) -> float:
        """计算信噪比."""
        values = np.array(values)
        signal_power = np.mean(values ** 2)
        noise_power = np.var(values)
        if noise_power < 1e-10:
            return 100.0
        return 10.0 * np.log10(signal_power / noise_power)

    def _calculate_spectral_flatness(self, values: List[float]) -> float:
        """计算谱平坦度."""
        values = np.array(values)
        if len(values) < 2:
            return 0.0
        # 使用几何平均/算术平均
        geo_mean = np.exp(np.mean(np.log(np.abs(values) + 1e-10)))
        arith_mean = np.mean(np.abs(values))
        return geo_mean / (arith_mean + 1e-10)

    def _calculate_low_freq_noise(self, values: List[float]) -> float:
        """计算低频噪声."""
        values = np.array(values)
        if len(values) < 4:
            return 0.0
        # 使用低频成分的方差占比
        diff = np.diff(values)
        return float(np.var(diff) / (np.var(values) + 1e-10))

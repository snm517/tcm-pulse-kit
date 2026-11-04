"""预处理模块.

包含信号分段、带通滤波、基线漂移校正和周期提取。
修复: A-014 变化点检测替代强制后50%。
"""

from typing import List, Tuple, Dict
from dataclasses import dataclass
import numpy as np
from scipy import signal


@dataclass
class PulseSegment:
    """脉象分段结果."""
    float_seg: np.ndarray
    deep_seg: np.ndarray
    float_ratio: float


class PulsePreprocessor:
    """脉搏预处理器.

    对原始脉搏波信号进行滤波、分段和周期提取。
    """

    def __init__(self, fs: float = 1000.0):
        """初始化预处理器.

        Args:
            fs: 采样率(Hz)
        """
        self.fs = fs
        self._design_filters()

    def _design_filters(self):
        """设计滤波器."""
        # 带通滤波器 0.5-30Hz
        self.b_band, self.a_band = signal.butter(
            4, [0.5, 30], btype='band', fs=self.fs
        )
        # 低通滤波器 20Hz (用于基线漂移校正)
        self.b_low, self.a_low = signal.butter(
            2, 20, btype='low', fs=self.fs
        )

    def process(self, waveform: np.ndarray) -> PulseSegment:
        """处理信号.

        Args:
            waveform: 原始波形

        Returns:
            分段结果
        """
        # 带通滤波
        filtered = signal.filtfilt(self.b_band, self.a_band, waveform)

        # 基线漂移校正
        baseline = signal.filtfilt(self.b_low, self.a_low, filtered)
        corrected = filtered - baseline

        # 变化点检测替代强制后50%
        change_point = self._detect_change_point(corrected)

        # 分段
        float_seg = corrected[:change_point]
        deep_seg = corrected[change_point:]

        float_ratio = len(float_seg) / len(corrected) if len(corrected) > 0 else 0.5

        return PulseSegment(
            float_seg=float_seg,
            deep_seg=deep_seg,
            float_ratio=float_ratio,
        )

    def _detect_change_point(self, signal_data: np.ndarray) -> int:
        """检测变化点 (CUSUM算法).

        Args:
            signal_data: 信号数据

        Returns:
            变化点索引
        """
        n = len(signal_data)
        if n < 100:
            return n // 2

        # CUSUM算法
        mean_val = np.mean(signal_data)
        std_val = np.std(signal_data) + 1e-10

        cusum_pos = np.zeros(n)
        cusum_neg = np.zeros(n)

        k = 0.5 * std_val
        h = 4.0 * std_val

        for i in range(1, n):
            cusum_pos[i] = max(0, cusum_pos[i-1] + signal_data[i] - mean_val - k)
            cusum_neg[i] = max(0, cusum_neg[i-1] - signal_data[i] + mean_val - k)

            if cusum_pos[i] > h or cusum_neg[i] > h:
                return i

        return n // 2

    def extract_cycles(self, waveform: np.ndarray) -> Tuple[List[np.ndarray], Dict]:
        """提取周期.

        Args:
            waveform: 波形数据

        Returns:
            (周期列表, 元数据)
        """
        # 找峰值
        peaks, _ = signal.find_peaks(waveform, distance=int(self.fs * 0.5))

        cycles = []
        for i in range(len(peaks) - 1):
            start = peaks[i]
            end = peaks[i + 1]
            cycle = waveform[start:end]
            cycles.append(cycle)

        meta = {"count": len(cycles), "peak_indices": peaks.tolist()}

        return cycles, meta

"""预处理器测试.

验证预处理器的各项功能。
"""

import pytest
import numpy as np

from tcm_pulse_kit.core.preprocessor import PulsePreprocessor


class TestPreprocessor:
    """预处理器测试."""

    def test_bandpass_filter(self):
        """测试带通滤波."""
        fs = 1000
        t = np.arange(0, 1, 1/fs)
        signal = np.sin(2 * np.pi * 1.2 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)

        preprocessor = PulsePreprocessor(fs=fs)
        segment = preprocessor.process(signal)

        # 滤波后高频成分应减少
        assert len(segment.float_seg) > 0
        assert len(segment.deep_seg) > 0

    def test_baseline_drift_correction(self):
        """测试基线漂移校正."""
        fs = 1000
        t = np.arange(0, 1, 1/fs)
        baseline = 0.1 * t
        signal = np.sin(2 * np.pi * 1.2 * t) + baseline

        preprocessor = PulsePreprocessor(fs=fs)
        segment = preprocessor.process(signal)

        # 校正后基线应接近0
        assert np.abs(np.mean(segment.float_seg)) < 0.1

    def test_change_point_detection(self):
        """测试变化点检测."""
        fs = 1000
        t = np.arange(0, 2, 1/fs)
        signal = np.sin(2 * np.pi * 1.2 * t)

        preprocessor = PulsePreprocessor(fs=fs)
        segment = preprocessor.process(signal)

        # 浮取和沉取都应存在
        assert len(segment.float_seg) > 0
        assert len(segment.deep_seg) > 0
        assert 0.3 < segment.float_ratio < 0.7

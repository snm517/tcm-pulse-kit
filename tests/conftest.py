"""测试配置.

提供测试用例的通用配置和Fixture。
"""

import pytest
import numpy as np


@pytest.fixture
def sample_signal():
    """创建模拟脉搏信号."""
    fs = 1000
    t = np.arange(0, 10, 1/fs)
    signal = np.sin(2 * np.pi * 1.2 * t) * np.exp(-((t % (1/1.2)) * 3))
    signal += 0.05 * np.random.randn(len(signal))
    return signal, fs


@pytest.fixture
def sample_features():
    """创建模拟特征数据."""
    return {
        "左寸": {"peak_amp": 1.0, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
        "左关": {"peak_amp": 1.5, "rise_ms": 120, "fall_ms": 220, "fwhm_ms": 170, "area": 60, "length": 350},
        "左尺": {"peak_amp": 0.9, "rise_ms": 105, "fall_ms": 210, "fwhm_ms": 155, "area": 48, "length": 295},
        "右寸": {"peak_amp": 1.1, "rise_ms": 98, "fall_ms": 195, "fwhm_ms": 148, "area": 52, "length": 305},
        "右关": {"peak_amp": 1.0, "rise_ms": 102, "fall_ms": 205, "fwhm_ms": 152, "area": 50, "length": 300},
        "右尺": {"peak_amp": 0.95, "rise_ms": 99, "fall_ms": 198, "fwhm_ms": 149, "area": 49, "length": 298},
    }

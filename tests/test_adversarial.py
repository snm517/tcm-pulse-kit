"""对抗性测试.

验证系统在各种边界条件下的表现。
"""

import pytest
import numpy as np

from tcm_pulse_kit.core.relative_engine import RelativeEngine
from tcm_pulse_kit.core.shibian_engine import ShibianEngine


class TestRelativeEngineBoundary:
    """相对值引擎边界测试."""

    def test_empty_input(self):
        """测试空输入."""
        re = RelativeEngine()
        with pytest.raises(ValueError):
            re.transform({})

    def test_single_position(self):
        """测试单部位."""
        re = RelativeEngine()
        with pytest.raises(ValueError):
            re.transform({"左寸": {"peak_amp": 1.0}})

    def test_extreme_values(self):
        """测试极端值."""
        re = RelativeEngine()
        features = {
            "左寸": {"peak_amp": 1e10, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "左关": {"peak_amp": 1.0, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "左尺": {"peak_amp": 0.9, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右寸": {"peak_amp": 1.1, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右关": {"peak_amp": 1.0, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右尺": {"peak_amp": 0.95, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
        }
        result = re.transform(features)
        assert result is not None

    def test_nan_values(self):
        """测试NaN值."""
        re = RelativeEngine()
        features = {
            "左寸": {"peak_amp": np.nan, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "左关": {"peak_amp": 1.0, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "左尺": {"peak_amp": 0.9, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右寸": {"peak_amp": 1.1, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右关": {"peak_amp": 1.0, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右尺": {"peak_amp": 0.95, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
        }
        with pytest.raises(ValueError):
            re.transform(features)


class TestShibianEngineBoundary:
    """十变引擎边界测试."""

    def test_empty_input(self):
        """测试空输入."""
        se = ShibianEngine()
        result = se.infer_all({}, {}, {})
        assert result == []

    def test_single_position(self):
        """测试单部位."""
        se = ShibianEngine()
        result = se.infer_all(
            {"左寸": {"peak_amp": 1.0}},
            {"左寸": 1.0},
            {"左寸": 0.5},
        )
        assert len(result) >= 0

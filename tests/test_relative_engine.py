"""相对值引擎测试.

验证相对值计算的各项功能。
"""

import pytest
import numpy as np

from tcm_pulse_kit.core.relative_engine import RelativeEngine


class TestRelativeEngine:
    """相对值引擎测试."""

    def test_winsorization(self):
        """测试Winsorization."""
        re = RelativeEngine()
        features = {
            "左寸": {"peak_amp": 1e10, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "左关": {"peak_amp": 1.0, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "左尺": {"peak_amp": 0.9, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右寸": {"peak_amp": 1.1, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右关": {"peak_amp": 1.0, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右尺": {"peak_amp": 0.95, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
        }
        fingerprint = re.transform(features)

        # 极端值应被缩尾处理
        z_scores = list(fingerprint.z_scores.values())
        assert all(abs(z) <= re.MAX_Z_SCORE for z in z_scores)

    def test_z_score_clipping(self):
        """测试z-score裁剪."""
        re = RelativeEngine()
        features = {
            "左寸": {"peak_amp": 10.0, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "左关": {"peak_amp": 1.0, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "左尺": {"peak_amp": 0.9, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右寸": {"peak_amp": 1.1, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右关": {"peak_amp": 1.0, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
            "右尺": {"peak_amp": 0.95, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
        }
        fingerprint = re.transform(features)

        # z-score应被裁剪到合理范围
        z_scores = list(fingerprint.z_scores.values())
        assert all(abs(z) <= re.MAX_Z_SCORE for z in z_scores)

"""十变引擎测试.

验证十变推理的各项功能。
"""

import pytest

from tcm_pulse_kit.core.shibian_engine import ShibianEngine


class TestShibianEngine:
    """十变引擎测试."""

    def test_init(self):
        """测试初始化."""
        se = ShibianEngine()
        assert se is not None
        assert len(se.wutai_weights) == 5

    def test_infer_ji(self):
        """测试急态推理."""
        se = ShibianEngine()
        raw_features = {
            "左寸": {"peak_amp": 2.0, "rise_ms": 50, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
        }
        z_scores = {"左寸": 2.0}
        fdr_values = {"左寸": 0.5}

        results = se.infer_all(raw_features, z_scores, fdr_values)
        assert any(r.state == "急" for r in results)

    def test_infer_chen(self):
        """测试沉态推理."""
        se = ShibianEngine()
        raw_features = {
            "左寸": {"peak_amp": 0.5, "rise_ms": 100, "fall_ms": 200, "fwhm_ms": 150, "area": 50, "length": 300},
        }
        z_scores = {"左寸": 0.0}
        fdr_values = {"左寸": 2.0}

        results = se.infer_all(raw_features, z_scores, fdr_values)
        assert any(r.state == "沉" for r in results)

    def test_weight_config(self):
        """测试权重配置."""
        se = ShibianEngine()
        assert "急" in se.wutai_weights
        assert "大" in se.wutai_weights
        assert "缓" in se.wutai_weights
        assert "涩" in se.wutai_weights
        assert "沉" in se.wutai_weights

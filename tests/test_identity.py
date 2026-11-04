"""身份验证测试.

验证系统的基本功能和身份。
"""

import pytest
import numpy as np

from tcm_pulse_kit import __version__
from tcm_pulse_kit.core.preprocessor import PulsePreprocessor
from tcm_pulse_kit.core.feature_extractor import CycleFeatureExtractor
from tcm_pulse_kit.core.relative_engine import RelativeEngine


class TestVersion:
    """版本测试."""

    def test_version(self):
        """测试版本号."""
        assert __version__ == "0.2.0"


class TestPreprocessor:
    """预处理器测试."""

    def test_init(self):
        """测试初始化."""
        preprocessor = PulsePreprocessor(fs=1000)
        assert preprocessor.fs == 1000

    def test_process(self, sample_signal):
        """测试处理."""
        signal, fs = sample_signal
        preprocessor = PulsePreprocessor(fs=fs)
        segment = preprocessor.process(signal)
        assert len(segment.float_seg) > 0
        assert len(segment.deep_seg) > 0

    def test_extract_cycles(self, sample_signal):
        """测试周期提取."""
        signal, fs = sample_signal
        preprocessor = PulsePreprocessor(fs=fs)
        segment = preprocessor.process(signal)
        cycles, meta = preprocessor.extract_cycles(segment.deep_seg)
        assert isinstance(cycles, list)
        assert "count" in meta


class TestFeatureExtractor:
    """特征提取器测试."""

    def test_init(self):
        """测试初始化."""
        extractor = CycleFeatureExtractor(fs=1000)
        assert extractor.fs == 1000

    def test_extract(self):
        """测试特征提取."""
        extractor = CycleFeatureExtractor(fs=1000)
        cycle = np.sin(np.linspace(0, np.pi, 100))
        features = extractor.extract(cycle)
        assert features.peak_amp > 0
        assert features.rise_ms > 0
        assert features.fall_ms > 0


class TestRelativeEngine:
    """相对值引擎测试."""

    def test_init(self):
        """测试初始化."""
        re = RelativeEngine()
        assert re is not None

    def test_transform(self, sample_features):
        """测试转换."""
        re = RelativeEngine()
        fingerprint = re.transform(sample_features)
        assert len(fingerprint.z_scores) == 6
        assert len(fingerprint.fdr_values) == 6

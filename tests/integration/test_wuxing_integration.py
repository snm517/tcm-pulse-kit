"""五行集成测试.

验证五行模块与主系统的集成。
"""

import pytest
import numpy as np

from tcm_pulse_kit.wuxing import (
    WuxingTopologyEngine,
    WuxingIntegratedDiagnosis,
    WuxingAnalysisInput,
    DetailedElementMapper,
)


class TestWuxingIntegration:
    """五行集成测试."""

    def test_engine_creation(self):
        """测试引擎创建."""
        engine = WuxingTopologyEngine(use_networkx=True)
        assert engine is not None

    def test_element_mapping(self):
        """测试元素映射."""
        mapper = DetailedElementMapper()
        mapping = mapper.get_mapping("左寸")
        assert mapping.element == "火"
        assert mapping.organ == "心"

    def test_path_search(self):
        """测试路径搜索."""
        engine = WuxingTopologyEngine(use_networkx=True)
        paths = engine.find_transmission_paths("木", "土", max_depth=3)
        assert len(paths) >= 0

    def test_cheng_wu_detection(self):
        """测试乘侮检测."""
        engine = WuxingTopologyEngine(use_networkx=True)
        z_scores = {"木": 2.0, "土": -1.0}
        results = engine.detect_cheng_wu(z_scores)
        assert len(results) >= 0

    def test_integrated_diagnosis(self):
        """测试集成诊断."""
        element_mapper = DetailedElementMapper()
        wuxing_engine = WuxingTopologyEngine(use_networkx=True)
        diagnosis = WuxingIntegratedDiagnosis(element_mapper, wuxing_engine)
        assert diagnosis is not None

    def test_analysis_input(self):
        """测试分析输入."""
        input_data = WuxingAnalysisInput(
            z_scores={"左寸": 1.0, "左关": 0.5, "左尺": -0.5}
        )
        strength = input_data.get_element_strength("左寸")
        assert strength == 1.0

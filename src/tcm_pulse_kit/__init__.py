"""TCM Pulse Kit - 中医脉象分析工具包.

支持六部脉象特征提取、相对值分析、十变推理和五行拓扑引擎。
"""

__version__ = "0.2.0"

from .pipeline import PulseDiagnosisPipeline
from .core.preprocessor import PulsePreprocessor
from .core.feature_extractor import CycleFeatureExtractor
from .core.relative_engine import RelativeEngine
from .core.shibian_engine import ShibianEngine
from .core.quality_gate import QualityGate

# 五行模块
from .wuxing.topology_engine import WuxingTopologyEngine
from .wuxing.integration import WuxingIntegratedDiagnosis
from .wuxing.data_flow import WuxingAnalysisInput
from .wuxing.element_mapping import DetailedElementMapper

__all__ = [
    "PulseDiagnosisPipeline",
    "PulsePreprocessor",
    "CycleFeatureExtractor",
    "RelativeEngine",
    "ShibianEngine",
    "QualityGate",
    "WuxingTopologyEngine",
    "WuxingIntegratedDiagnosis",
    "WuxingAnalysisInput",
    "DetailedElementMapper",
]

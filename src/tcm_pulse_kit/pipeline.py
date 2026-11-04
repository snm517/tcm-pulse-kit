"""端到端诊断流水线."""

from typing import Dict, List, Optional
import numpy as np

from .core.preprocessor import PulsePreprocessor
from .core.feature_extractor import CycleFeatureExtractor
from .core.relative_engine import RelativeEngine
from .core.shibian_engine import ShibianEngine
from .core.quality_gate import QualityGate


class PulseDiagnosisPipeline:
    """脉搏诊断流水线.

    整合预处理、特征提取、相对值分析、十变推理和质量门禁。
    """

    def __init__(self, fs: float = 1000.0):
        """初始化流水线.

        Args:
            fs: 采样率(Hz)
        """
        self.fs = fs
        self.preprocessor = PulsePreprocessor(fs=fs)
        self.extractor = CycleFeatureExtractor(fs=fs)
        self.relative_engine = RelativeEngine()
        self.shibian_engine = ShibianEngine()
        self.quality_gate = QualityGate()

    def run(self, pulse_input) -> "PulseDiagnosisReport":
        """运行完整诊断流程.

        Args:
            pulse_input: 脉搏输入数据

        Returns:
            诊断报告
        """
        features_by_pos: Dict[str, List[Dict]] = {}

        for position, channel in pulse_input.channels.items():
            segment = self.preprocessor.process(channel.waveform)
            cycles, meta = self.preprocessor.extract_cycles(segment.deep_seg)

            features = []
            for cycle in cycles:
                feat = self.extractor.extract(cycle)
                features.append(feat.to_dict())

            features_by_pos[position] = features

        # 质量门禁
        quality_result = self.quality_gate.evaluate(features_by_pos)

        # 相对值分析
        medians = {pos: self._median_features(feats) for pos, feats in features_by_pos.items()}
        fingerprint = self.relative_engine.transform(medians)

        # 十变推理
        shibian_results = self.shibian_engine.infer_all(
            medians, fingerprint.z_scores, fingerprint.fdr_values
        )

        return PulseDiagnosisReport(
            overall_confidence=quality_result.overall_confidence,
            shibian=shibian_results,
            quality_flags=quality_result.flags,
            pathogenesis_chains=[],
        )

    def _median_features(self, features: List[Dict]) -> Dict:
        """计算特征中位数."""
        if not features:
            return {}

        result = {}
        for key in features[0].keys():
            values = [f[key] for f in features if key in f]
            result[key] = float(np.median(values)) if values else 0.0
        return result


class PulseDiagnosisReport:
    """诊断报告."""

    def __init__(
        self,
        overall_confidence: float,
        shibian: List,
        quality_flags: List[str],
        pathogenesis_chains: List[str],
    ):
        self.overall_confidence = overall_confidence
        self.shibian = shibian
        self.quality_flags = quality_flags
        self.pathogenesis_chains = pathogenesis_chains

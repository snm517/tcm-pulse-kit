"""证据融合模块.

提供多源证据的融合和推理。
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class Evidence:
    """证据."""
    source: str
    hypothesis: str
    confidence: float
    weight: float = 1.0


class EvidenceFusion:
    """证据融合器.

    融合来自多个源的证据。
    """

    def __init__(self):
        """初始化融合器."""
        self.evidences = []

    def add_evidence(self, evidence: Evidence) -> None:
        """添加证据.

        Args:
            evidence: 证据对象
        """
        self.evidences.append(evidence)

    def fuse(self) -> Dict[str, float]:
        """融合证据.

        Returns:
            融合后的假设置信度字典
        """
        if not self.evidences:
            return {}

        # 按假设分组
        hypothesis_confidences = {}
        hypothesis_weights = {}

        for ev in self.evidences:
            h = ev.hypothesis
            if h not in hypothesis_confidences:
                hypothesis_confidences[h] = 0.0
                hypothesis_weights[h] = 0.0

            hypothesis_confidences[h] += ev.confidence * ev.weight
            hypothesis_weights[h] += ev.weight

        # 加权平均
        result = {}
        for h in hypothesis_confidences:
            if hypothesis_weights[h] > 0:
                result[h] = hypothesis_confidences[h] / hypothesis_weights[h]

        return result

    def get_best_hypothesis(self) -> Optional[str]:
        """获取最佳假设.

        Returns:
            最佳假设
        """
        fused = self.fuse()
        if not fused:
            return None
        return max(fused, key=fused.get)

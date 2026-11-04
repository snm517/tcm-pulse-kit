"""五行数据流模块.

管理五行分析的数据流和输入数据结构。
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class WuxingAnalysisInput:
    """五行分析输入.

    包含诊断报告、脉象指纹和原始特征。
    """

    diagnosis_report: Optional[Any] = None
    fingerprint: Optional[Any] = None
    raw_features: Optional[Dict] = None
    z_scores: Optional[Dict[str, float]] = None

    def get_element_strength(self, position: str) -> float:
        """获取指定部位的五行强度.

        Args:
            position: 部位名称

        Returns:
            强度值 (z-score)
        """
        if self.z_scores and position in self.z_scores:
            return self.z_scores[position]
        return 0.0


class WuxingDataFlowManager:
    """五行数据流管理器.

    管理数据在系统间的流动。
    """

    def prepare_input(
        self,
        diagnosis_output: Any,
        fingerprint: Any,
        raw_features: Optional[Dict] = None,
    ) -> WuxingAnalysisInput:
        """准备五行分析输入.

        Args:
            diagnosis_output: 诊断输出
            fingerprint: 脉象指纹
            raw_features: 原始特征

        Returns:
            五行分析输入
        """
        z_scores = {}
        if hasattr(fingerprint, 'z_scores'):
            z_scores = fingerprint.z_scores

        return WuxingAnalysisInput(
            diagnosis_report=diagnosis_output,
            fingerprint=fingerprint,
            raw_features=raw_features,
            z_scores=z_scores,
        )

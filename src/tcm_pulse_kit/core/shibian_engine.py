"""十变推理引擎.

根据相对值推理急、大、缓、涩、沉五态。
修复: T-004 权重从YAML加载。
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import os
import yaml


@dataclass
class ShibianResult:
    """十变结果."""
    position: str
    state: str
    confidence: float


class ShibianEngine:
    """十变推理引擎.

    根据z-score和fdr推理五态。
    """

    def __init__(self, config_path: Optional[str] = None):
        """初始化引擎.

        Args:
            config_path: 权重配置文件路径
        """
        self.wutai_weights = self._load_weights(config_path)

    def _load_weights(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """加载权重配置.

        Args:
            config_path: 配置文件路径

        Returns:
            权重字典
        """
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)

        # 默认权重
        return {
            "急": {"z_threshold": 1.5, "fdr_threshold": 0.5, "weight": 1.0},
            "大": {"z_threshold": 1.0, "fdr_threshold": 0.3, "weight": 1.0},
            "缓": {"z_threshold": -1.0, "fdr_threshold": -0.3, "weight": 1.0},
            "涩": {"z_threshold": -1.5, "fdr_threshold": -0.5, "weight": 1.0},
            "沉": {"z_threshold": 0.0, "fdr_threshold": 1.0, "weight": 1.0},
        }

    def infer_all(
        self,
        raw_features: Dict[str, Dict],
        z_scores: Dict[str, float],
        fdr_values: Dict[str, float],
    ) -> List[ShibianResult]:
        """推理所有部位的五态.

        Args:
            raw_features: 原始特征
            z_scores: z-score字典
            fdr_values: fdr值字典

        Returns:
            十变结果列表
        """
        results = []

        for position in z_scores.keys():
            z = z_scores.get(position, 0.0)
            fdr = fdr_values.get(position, 0.0)

            # 五态判定
            for state, config in self.wutai_weights.items():
                z_th = config.get("z_threshold", 0.0)
                fdr_th = config.get("fdr_threshold", 0.0)
                weight = config.get("weight", 1.0)

                if state == "沉":
                    # 沉态判定：fdr > threshold
                    if fdr > fdr_th:
                        confidence = min(1.0, abs(fdr) * weight)
                        results.append(ShibianResult(position, state, confidence))
                elif state == "急":
                    # 急态判定：z > threshold
                    if z > z_th:
                        confidence = min(1.0, abs(z) * weight)
                        results.append(ShibianResult(position, state, confidence))
                elif state == "大":
                    # 大态判定：z > threshold
                    if z > z_th:
                        confidence = min(1.0, abs(z) * weight)
                        results.append(ShibianResult(position, state, confidence))
                elif state == "缓":
                    # 缓态判定：z < threshold
                    if z < z_th:
                        confidence = min(1.0, abs(z) * weight)
                        results.append(ShibianResult(position, state, confidence))
                elif state == "涩":
                    # 涩态判定：z < threshold
                    if z < z_th:
                        confidence = min(1.0, abs(z) * weight)
                        results.append(ShibianResult(position, state, confidence))

        # 按置信度排序
        results.sort(key=lambda x: x.confidence, reverse=True)

        return results

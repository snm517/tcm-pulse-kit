"""五行集成模块.

提供五行分析与主系统的集成功能。
"""

from typing import Dict, List, Optional, Any
import numpy as np

from .topology_engine import WuxingTopologyEngine, RelationType
from .element_mapping import DetailedElementMapper
from .data_flow import WuxingAnalysisInput


class WuxingIntegratedDiagnosis:
    """五行集成诊断器.

    将五行拓扑引擎集成到脉象诊断流程中。
    """

    def __init__(
        self,
        element_mapper: Optional[DetailedElementMapper] = None,
        wuxing_engine: Optional[WuxingTopologyEngine] = None,
    ):
        """初始化诊断器.

        Args:
            element_mapper: 五行映射器
            wuxing_engine: 五行拓扑引擎
        """
        self.element_mapper = element_mapper or DetailedElementMapper()
        self.wuxing_engine = wuxing_engine or WuxingTopologyEngine()

    def enhance_diagnosis(
        self,
        diagnosis_output: Any,
        analysis_input: WuxingAnalysisInput,
    ) -> Any:
        """增强诊断报告.

        Args:
            diagnosis_output: 原始诊断输出
            analysis_input: 五行分析输入

        Returns:
            增强后的诊断输出
        """
        # 1. 转换为五行元素强度
        element_strengths = self._convert_to_elements(analysis_input)

        # 2. 五行分析
        pathogenesis = self.wuxing_engine.analyze_pathogenesis(element_strengths)
        treatment = self.wuxing_engine.recommend_treatment(pathogenesis)

        # 3. 增强报告
        self._enhance_report(diagnosis_output, pathogenesis, treatment)

        return diagnosis_output

    def _convert_to_elements(self, analysis_input: WuxingAnalysisInput) -> Dict[str, float]:
        """转换为五行元素强度.

        Args:
            analysis_input: 分析输入

        Returns:
            五行元素强度字典
        """
        element_strengths = {}

        for position in analysis_input.z_scores.keys():
            mapping = self.element_mapper.get_mapping(position)
            if not mapping:
                continue

            element = mapping.element
            strength = analysis_input.get_element_strength(position)

            if element in element_strengths:
                element_strengths[element] = max(element_strengths[element], strength)
            else:
                element_strengths[element] = strength

        return element_strengths

    def _enhance_report(
        self,
        diagnosis_output: Any,
        pathogenesis: List,
        treatment: List[Dict[str, str]],
    ) -> None:
        """增强报告.

        Args:
            diagnosis_output: 诊断输出
            pathogenesis: 病机分析结果
            treatment: 治疗建议
        """
        # 添加五行分析
        diagnosis_output.quality_flags.append("")
        diagnosis_output.quality_flags.append("【五行拓扑分析】")

        for p in pathogenesis[:5]:
            diagnosis_output.quality_flags.append(f"  {p.description}")

        # 添加治疗建议
        if treatment:
            diagnosis_output.quality_flags.append("")
            diagnosis_output.quality_flags.append("【治疗建议】")

            for t in treatment[:3]:
                diagnosis_output.quality_flags.append(f"  {t['principle']}: {t['method']}")

        # 更新病机传导链
        for p in pathogenesis:
            if p.type == "传变":
                path_str = "→".join(p.path)
                chain_desc = f"{p.source}传{p.target}（{path_str}）"

                if chain_desc not in diagnosis_output.pathogenesis_chains:
                    diagnosis_output.pathogenesis_chains.append(chain_desc)

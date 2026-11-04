"""结构化输出模块.

提供五行分析的结构化输出和格式化。
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class WuxingAnalysisOutput:
    """五行分析输出.

    结构化的五行分析结果。
    """

    element_strengths: Dict[str, float]
    pathogenesis: List[Dict[str, Any]]
    treatment: List[Dict[str, str]]
    transmission_paths: List[List[str]]
    cheng_wu_relations: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典."""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """转换为JSON字符串."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class WuxingReportFormatter:
    """五行报告格式化器.

    将五行分析结果格式化为人类可读的报告。
    """

    def format(self, output: WuxingAnalysisOutput) -> str:
        """格式化报告.

        Args:
            output: 五行分析输出

        Returns:
            格式化后的报告
        """
        lines = []
        lines.append("=" * 50)
        lines.append("五行拓扑分析报告")
        lines.append("=" * 50)

        # 元素强度
        lines.append("\n【五行元素强度】")
        for element, strength in sorted(output.element_strengths.items()):
            state = "亢盛" if strength > 1.0 else "虚弱" if strength < -1.0 else "正常"
            lines.append(f"  {element}: {strength:.2f} ({state})")

        # 病机分析
        if output.pathogenesis:
            lines.append("\n【病机分析】")
            for p in output.pathogenesis[:5]:
                lines.append(f"  {p.get('description', '')}")

        # 治疗建议
        if output.treatment:
            lines.append("\n【治疗建议】")
            for t in output.treatment[:3]:
                lines.append(f"  {t.get('principle', '')}: {t.get('method', '')}")

        # 传变路径
        if output.transmission_paths:
            lines.append("\n【传变路径】")
            for path in output.transmission_paths[:3]:
                lines.append(f"  {' → '.join(path)}")

        # 乘侮关系
        if output.cheng_wu_relations:
            lines.append("\n【乘侮关系】")
            for r in output.cheng_wu_relations[:3]:
                lines.append(f"  {r.get('description', '')}")

        lines.append("\n" + "=" * 50)

        return "\n".join(lines)

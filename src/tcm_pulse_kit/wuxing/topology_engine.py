"""五行拓扑引擎.

实现五行生克乘侮关系的拓扑分析和病机传变路径搜索。
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np


class RelationType(Enum):
    """关系类型."""
    SHENG = "生"  # 相生
    KE = "克"     # 相克
    CHENG = "乘"  # 相乘
    WU = "侮"     # 相侮


@dataclass
class PathogenesisResult:
    """病机结果."""
    type: str
    source: str
    target: str
    path: List[str]
    description: str
    confidence: float


@dataclass
class TransmissionPath:
    """传变路径."""
    path: List[str]
    relations: List[RelationType]
    strength: float


class WuxingTopologyEngine:
    """五行拓扑引擎.

    实现五行生克乘侮关系的完整拓扑分析。
    """

    # 五行元素
    ELEMENTS = ["木", "火", "土", "金", "水"]

    # 相生关系 (我生者)
    SHENG_MAP = {
        "木": "火",
        "火": "土",
        "土": "金",
        "金": "水",
        "水": "木",
    }

    # 相克关系 (我克者)
    KE_MAP = {
        "木": "土",
        "土": "水",
        "水": "火",
        "火": "金",
        "金": "木",
    }

    # 相乘关系 (乘我者 - 过度克制)
    CHENG_MAP = {
        "木": "金",
        "火": "水",
        "土": "木",
        "金": "火",
        "水": "土",
    }

    # 相侮关系 (侮我者 - 反向克制)
    WU_MAP = {
        "木": "土",
        "火": "金",
        "土": "水",
        "金": "木",
        "水": "火",
    }

    def __init__(self, use_networkx: bool = True):
        """初始化引擎.

        Args:
            use_networkx: 是否使用NetworkX
        """
        self.use_networkx = use_networkx
        self._graph = None
        if use_networkx:
            try:
                import networkx as nx
                self._build_graph(nx)
            except ImportError:
                self.use_networkx = False

    def _build_graph(self, nx):
        """构建五行图."""
        self._graph = nx.DiGraph()

        # 添加节点
        for element in self.ELEMENTS:
            self._graph.add_node(element)

        # 添加相生边
        for source, target in self.SHENG_MAP.items():
            self._graph.add_edge(source, target, relation=RelationType.SHENG, weight=1.0)

        # 添加相克边
        for source, target in self.KE_MAP.items():
            self._graph.add_edge(source, target, relation=RelationType.KE, weight=-1.0)

    def get_attacker(self, element: str, relation: RelationType) -> Optional[str]:
        """获取克制指定元素的元素.

        Args:
            element: 被克制的元素
            relation: 关系类型

        Returns:
            克制者元素
        """
        if relation == RelationType.KE:
            # 我克者
            for k, v in self.KE_MAP.items():
                if v == element:
                    return k
        elif relation == RelationType.CHENG:
            # 乘我者
            return self.CHENG_MAP.get(element)
        elif relation == RelationType.WU:
            # 侮我者
            return self.WU_MAP.get(element)
        return None

    def find_transmission_paths(
        self,
        source: str,
        target: str,
        max_depth: int = 3,
    ) -> List[TransmissionPath]:
        """查找传变路径.

        Args:
            source: 起始元素
            target: 目标元素
            max_depth: 最大搜索深度

        Returns:
            传变路径列表
        """
        if self.use_networkx and self._graph is not None:
            return self._find_paths_networkx(source, target, max_depth)
        return self._find_paths_manual(source, target, max_depth)

    def _find_paths_networkx(self, source: str, target: str, max_depth: int) -> List[TransmissionPath]:
        """使用NetworkX查找路径."""
        import networkx as nx

        paths = []
        try:
            for path in nx.all_simple_paths(self._graph, source, target, cutoff=max_depth):
                relations = []
                for i in range(len(path) - 1):
                    edge_data = self._graph.get_edge_data(path[i], path[i+1])
                    relations.append(edge_data.get("relation", RelationType.SHENG))

                paths.append(TransmissionPath(
                    path=path,
                    relations=relations,
                    strength=1.0 / len(path),
                ))
        except nx.NetworkXNoPath:
            pass

        return paths

    def _find_paths_manual(self, source: str, target: str, max_depth: int) -> List[TransmissionPath]:
        """手动查找路径."""
        paths = []

        def dfs(current: str, target: str, path: List[str], depth: int):
            if depth > max_depth:
                return
            if current == target and len(path) > 1:
                relations = []
                for i in range(len(path) - 1):
                    if self.SHENG_MAP.get(path[i]) == path[i+1]:
                        relations.append(RelationType.SHENG)
                    elif self.KE_MAP.get(path[i]) == path[i+1]:
                        relations.append(RelationType.KE)
                    else:
                        relations.append(RelationType.SHENG)

                paths.append(TransmissionPath(
                    path=path.copy(),
                    relations=relations,
                    strength=1.0 / len(path),
                ))
                return

            # 探索相生和相克路径
            for next_elem in [self.SHENG_MAP.get(current), self.KE_MAP.get(current)]:
                if next_elem and next_elem not in path:
                    path.append(next_elem)
                    dfs(next_elem, target, path, depth + 1)
                    path.pop()

        dfs(source, target, [source], 0)
        return paths

    def analyze_pathogenesis(self, z_scores: Dict[str, float]) -> List[PathogenesisResult]:
        """分析病机.

        Args:
            z_scores: 五行z-score字典

        Returns:
            病机分析结果
        """
        results = []

        # 1. 检测五行失衡
        for element, z in z_scores.items():
            if abs(z) > 1.5:
                state = "亢盛" if z > 0 else "虚弱"
                results.append(PathogenesisResult(
                    type="失衡",
                    source=element,
                    target=element,
                    path=[element],
                    description=f"{element}{state} (z={z:.2f})",
                    confidence=min(1.0, abs(z) / 3.0),
                ))

        # 2. 检测乘侮关系
        cheng_wu = self.detect_cheng_wu(z_scores)
        for relation in cheng_wu:
            results.append(PathogenesisResult(
                type="传变",
                source=relation["source"],
                target=relation["target"],
                path=relation.get("path", []),
                description=relation["description"],
                confidence=relation.get("confidence", 0.5),
            ))

        # 按置信度排序
        results.sort(key=lambda x: x.confidence, reverse=True)

        return results

    def detect_cheng_wu(self, z_scores: Dict[str, float]) -> List[Dict]:
        """检测乘侮关系.

        Args:
            z_scores: 五行z-score字典

        Returns:
            乘侮关系列表
        """
        results = []

        for element, z in z_scores.items():
            if z > 1.0:  # 某行偏亢
                # 检测相乘
                cheng_target = self.KE_MAP.get(element)
                if cheng_target and cheng_target in z_scores:
                    target_z = z_scores[cheng_target]
                    if target_z < -0.5:  # 被克者虚弱
                        results.append({
                            "type": "相乘",
                            "source": element,
                            "target": cheng_target,
                            "path": [element, cheng_target],
                            "description": f"{element}乘{cheng_target}",
                            "confidence": min(1.0, abs(z) * abs(target_z) / 4.0),
                        })

                # 检测相侮
                wu_target = self.WU_MAP.get(element)
                if wu_target and wu_target in z_scores:
                    target_z = z_scores[wu_target]
                    if target_z > 0.5:  # 反克者偏亢
                        results.append({
                            "type": "相侮",
                            "source": element,
                            "target": wu_target,
                            "path": [element, wu_target],
                            "description": f"{element}侮{wu_target}",
                            "confidence": min(1.0, abs(z) * abs(target_z) / 4.0),
                        })

        return results

    def recommend_treatment(self, pathogenesis: List[PathogenesisResult]) -> List[Dict[str, str]]:
        """推荐治疗原则.

        Args:
            pathogenesis: 病机分析结果

        Returns:
            治疗建议列表
        """
        treatments = []

        for p in pathogenesis:
            if p.type == "失衡":
                if "亢盛" in p.description:
                    treatments.append({
                        "principle": "实则泻之",
                        "method": f"泻{p.source}",
                        "target": p.source,
                    })
                else:
                    treatments.append({
                        "principle": "虚则补之",
                        "method": f"补{p.source}",
                        "target": p.source,
                    })
            elif p.type == "传变":
                treatments.append({
                    "principle": "见肝之病，知肝传脾",
                    "method": f"先{p.target}后{p.source}",
                    "target": p.target,
                })

        # 去重
        seen = set()
        unique_treatments = []
        for t in treatments:
            key = (t["principle"], t["method"])
            if key not in seen:
                seen.add(key)
                unique_treatments.append(t)

        return unique_treatments

"""五行映射模块.

提供脉象部位到五行元素的映射关系。
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class PositionElementMapping:
    """部位五行映射."""
    position: str
    element: str
    organ: str
    hand: str


class DetailedElementMapper:
    """详细五行映射器.

    提供六部脉象到五行元素的详细映射。
    """

    # 六部脉象五行映射
    MAPPINGS = {
        "左寸": PositionElementMapping("左寸", "火", "心", "左手"),
        "左关": PositionElementMapping("左关", "木", "肝", "左手"),
        "左尺": PositionElementMapping("左尺", "水", "肾", "左手"),
        "右寸": PositionElementMapping("右寸", "金", "肺", "右手"),
        "右关": PositionElementMapping("右关", "土", "脾", "右手"),
        "右尺": PositionElementMapping("右尺", "水", "肾", "右手"),
    }

    def get_mapping(self, position: str) -> Optional[PositionElementMapping]:
        """获取指定部位的五行映射.

        Args:
            position: 部位名称

        Returns:
            映射关系
        """
        return self.MAPPINGS.get(position)

    def get_element(self, position: str) -> str:
        """获取指定部位的五行元素.

        Args:
            position: 部位名称

        Returns:
            五行元素
        """
        mapping = self.get_mapping(position)
        return mapping.element if mapping else ""

    def get_organ(self, position: str) -> str:
        """获取指定部位的脏腑.

        Args:
            position: 部位名称

        Returns:
            脏腑名称
        """
        mapping = self.get_mapping(position)
        return mapping.organ if mapping else ""

    def get_positions_by_element(self, element: str) -> list:
        """获取指定五行元素对应的所有部位.

        Args:
            element: 五行元素

        Returns:
            部位列表
        """
        return [pos for pos, mapping in self.MAPPINGS.items() if mapping.element == element]

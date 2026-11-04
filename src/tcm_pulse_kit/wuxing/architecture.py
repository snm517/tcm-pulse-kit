"""五行架构模块.

提供解耦架构和依赖注入支持。
"""

from typing import Dict, Type, Any, Optional


class DependencyRegistry:
    """依赖注册表.

    管理组件的依赖关系，支持依赖注入。
    """

    _instance = None
    _dependencies: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, name: str, instance: Any) -> None:
        """注册依赖.

        Args:
            name: 依赖名称
            instance: 依赖实例
        """
        self._dependencies[name] = instance

    def get(self, name: str) -> Optional[Any]:
        """获取依赖.

        Args:
            name: 依赖名称

        Returns:
            依赖实例
        """
        return self._dependencies.get(name)

    def clear(self) -> None:
        """清空注册表."""
        self._dependencies.clear()


class ComponentFactory:
    """组件工厂.

    负责创建和管理组件实例。
    """

    @staticmethod
    def create_wuxing_engine(use_networkx: bool = True):
        """创建五行引擎.

        Args:
            use_networkx: 是否使用NetworkX

        Returns:
            五行引擎实例
        """
        from .topology_engine import WuxingTopologyEngine
        return WuxingTopologyEngine(use_networkx=use_networkx)

    @staticmethod
    def create_element_mapper():
        """创建五行映射器.

        Returns:
            五行映射器实例
        """
        from .element_mapping import DetailedElementMapper
        return DetailedElementMapper()

    @staticmethod
    def create_integrated_diagnosis(element_mapper=None, wuxing_engine=None):
        """创建集成诊断器.

        Args:
            element_mapper: 五行映射器
            wuxing_engine: 五行引擎

        Returns:
            集成诊断器实例
        """
        from .integration import WuxingIntegratedDiagnosis
        return WuxingIntegratedDiagnosis(element_mapper, wuxing_engine)

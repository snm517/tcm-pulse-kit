"""依赖注入模块.

提供依赖注入容器。
"""

from typing import Dict, Type, Any, Optional, Callable


class DIContainer:
    """依赖注入容器.

    管理组件的创建和依赖关系。
    """

    _instance = None
    _registrations: Dict[str, Callable] = {}
    _singletons: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, name: str, factory: Callable, singleton: bool = False) -> None:
        """注册依赖.

        Args:
            name: 依赖名称
            factory: 工厂函数
            singleton: 是否为单例
        """
        self._registrations[name] = {"factory": factory, "singleton": singleton}

    def resolve(self, name: str) -> Any:
        """解析依赖.

        Args:
            name: 依赖名称

        Returns:
            依赖实例
        """
        if name in self._singletons:
            return self._singletons[name]

        if name not in self._registrations:
            raise KeyError(f"未注册的依赖: {name}")

        registration = self._registrations[name]
        instance = registration["factory"]()

        if registration["singleton"]:
            self._singletons[name] = instance

        return instance

    def clear(self) -> None:
        """清空容器."""
        self._registrations.clear()
        self._singletons.clear()

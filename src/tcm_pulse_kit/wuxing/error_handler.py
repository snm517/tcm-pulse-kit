"""错误处理模块.

提供五行模块的错误处理和日志记录。
"""

from typing import Optional, Any
import logging


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WuxingErrorHandler:
    """五行错误处理器.

    处理五行模块中的错误和异常。
    """

    def __init__(self):
        """初始化处理器."""
        self.errors = []
        self.warnings = []

    def handle_error(self, error: Exception, context: str = "") -> None:
        """处理错误.

        Args:
            error: 异常对象
            context: 错误上下文
        """
        error_msg = f"{context}: {str(error)}"
        self.errors.append(error_msg)
        logger.error(error_msg)

    def handle_warning(self, message: str, context: str = "") -> None:
        """处理警告.

        Args:
            message: 警告信息
            context: 警告上下文
        """
        warning_msg = f"{context}: {message}"
        self.warnings.append(warning_msg)
        logger.warning(warning_msg)

    def has_errors(self) -> bool:
        """是否有错误.

        Returns:
            是否有错误
        """
        return len(self.errors) > 0

    def get_errors(self) -> list:
        """获取所有错误.

        Returns:
            错误列表
        """
        return self.errors.copy()

    def get_warnings(self) -> list:
        """获取所有警告.

        Returns:
            警告列表
        """
        return self.warnings.copy()

    def clear(self) -> None:
        """清空错误和警告."""
        self.errors.clear()
        self.warnings.clear()

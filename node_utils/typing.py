from typing import (
    Callable,
    Optional,
    TypeVar,
    Union,
)

from node_utils.node import BaseNode, NodeClass, NodeAttr


ContextType = TypeVar("ContextType")
ReturnType = TypeVar("ReturnType")
FnType = TypeVar("FnType")
VisitFn = Callable[[BaseNode, Optional[ContextType]], None]
OptimizeFn = Callable[[BaseNode, Optional[ContextType]], Union[BaseNode, None]]
TransformFn = Callable[[BaseNode, Optional[ContextType]], ReturnType]

__all__ = [
    "BaseNode",
    "NodeClass",
    "NodeAttr",
    "VisitFn",
    "OptimizeFn",
    "TransformFn",
    "ContextType",
    "FnType",
    "ReturnType",
]

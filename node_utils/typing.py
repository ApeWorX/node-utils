from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    TypeVar,
    Union,
)

from node_utils.node import BaseNode, NodeClass, NodeAttr


Context = Optional[Dict[str, Any]]
OptimizedNode = Union[BaseNode, None]
ReturnType = TypeVar("ReturnType")
FnType = TypeVar("FnType")
VisitFn = Callable[[BaseNode, Context], None]
OptimizeFn = Callable[[BaseNode, Context], OptimizedNode]
TransformFn = Callable[[BaseNode, Context], ReturnType]

__all__ = [
    "BaseNode",
    "NodeClass",
    "NodeAttr",
    "Context",
    "VisitFn",
    "OptimizeFn",
    "TransformFn",
    "ReturnType",
]

from typing import (
    Callable,
    Optional,
    TypeVar,
)

from node_utils.node import BaseNode, NodeClass, NodeAttr


Context = TypeVar("Context")
ReturnType = TypeVar("ReturnType")
FnType = TypeVar("FnType")
VisitFn = Callable[[BaseNode, Optional[Context]], None]
MutateFn = Callable[[BaseNode, Optional[Context]], Optional[BaseNode]]
TransformFn = Callable[[BaseNode, Optional[Context]], ReturnType]

__all__ = [
    "BaseNode",
    "NodeClass",
    "NodeAttr",
    "Context",
    "VisitFn",
    "MutateFn",
    "TransformFn",
    "ReturnType",
]

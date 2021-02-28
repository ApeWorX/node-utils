from typing import (
    Callable,
    Optional,
    TypeVar,
    Union,
)

from node_utils.node import BaseNode, NodeClass, NodeAttr


ContextType = TypeVar("ContextType")
ReturnType = TypeVar("ReturnType")

VisitFn = Union[
    Callable[[BaseNode], None],
    Callable[[BaseNode, ContextType], None],
]
OptimizeFn = Union[
    Callable[[BaseNode], Optional[BaseNode]],
    Callable[[BaseNode, ContextType], Optional[BaseNode]],
]
TransformFn = Union[
    Callable[[BaseNode], ReturnType],
    Callable[[BaseNode, ContextType], ReturnType],
]

FnType = TypeVar("FnType", VisitFn, OptimizeFn, TransformFn)

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

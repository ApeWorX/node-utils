from typing import Callable, Optional, TypeVar

from node_utils.node import BaseNode, NodeAttr, NodeClass

ContextType = TypeVar("ContextType")
ReturnType = TypeVar("ReturnType")

VisitFn = Callable[[BaseNode, Optional[ContextType]], None]
OptimizeFn = Callable[[BaseNode, Optional[ContextType]], Optional[BaseNode]]
TransformFn = Callable[[BaseNode, Optional[ContextType]], ReturnType]

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

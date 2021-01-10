from typing import Dict, Generic, List, Optional, Union

from node_utils.errors import ExplorationError, RegistrationError
from node_utils.typing import (
    BaseNode,
    Context,
    NodeClass,
    NodeAttr,
    ReturnType,
    TransformFn,
)

from .base import BaseExplorer


class NodeTransformer(BaseExplorer[TransformFn, Context], Generic[ReturnType, Context]):
    """
    Transformer Generic class:
        visit and transform nodes in a tree-like structure of 'NodeClass'

        functions must be pure, with 'NodeClass' as input and 'ReturnType' as output

        There is no default (all nodes in tree must have transforms)
    """

    def transform(self, node: BaseNode, context: Optional[Context] = None) -> ReturnType:
        node_class = node.__class__

        if not isinstance(node, self._node_base_class):
            raise ExplorationError(f"'{node_class.__name__}' is not a '{self.node_class_name}'")

        elif node.__class__ in self._functions.keys():
            return self._functions[node_class](node, context)

        elif self._node_base_class in self._functions.keys():
            return self._functions[self._node_base_class](node, context)

        else:
            raise ExplorationError(f"Transform for '{node.__class__}' is not registered")

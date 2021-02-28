from typing import Generic, Optional

from node_utils.errors import ExplorationError
from node_utils.typing import BaseNode, ContextType, ReturnType, TransformFn

from .base import BaseExplorer


class NodeTransformer(BaseExplorer[TransformFn], Generic[ContextType, ReturnType]):
    """
    Transformer Generic class:
        visit and transform nodes in a tree-like structure of 'NodeClass'

        functions must be pure, with 'NodeClass' as input and 'ReturnType' as output

        There is no default (all nodes in tree must have transforms)
    """

    def transform(self, node: BaseNode, context: Optional[ContextType] = None) -> ReturnType:
        fn = self._get_registered_function(node)
        if fn is None:
            raise ExplorationError(f"Transform function not found for {node.__class__.__name__}")
        else:
            return fn(node, context)

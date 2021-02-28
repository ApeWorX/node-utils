from typing import Optional

from node_utils.errors import ExplorationError
from node_utils.typing import BaseNode, ContextType, VisitFn

from .base import BaseExplorer


class NodeVisitor(BaseExplorer[VisitFn]):
    """
    Visitor Generic class:
        visit and view nodes in a tree-like structure of 'NodeClass'

        functions must be pure, taking 'NodeClass' as input and return nothing
    """

    def visit(self, node: BaseNode, context: Optional[ContextType] = None):
        fn = self._get_registered_function(node) or self.__generic_visit
        fn(node, context)  # NOTE: Doesn't return anything

    def __generic_visit(self, node: BaseNode, context: ContextType):
        for attr, value in node.iter_attributes():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, self._node_base_class):
                        self.visit(item, context)

                    else:
                        raise ExplorationError(
                            f"Item {item} in '{attr}' of {node} is not of type"
                            f" {self.node_class_name}"
                        )

            elif isinstance(value, self._node_base_class):
                self.visit(value, context)

            else:
                raise ExplorationError(
                    f"'{attr}' of {node} is not a list or {self.node_class_name}"
                )

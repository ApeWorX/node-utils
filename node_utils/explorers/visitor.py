from typing import Dict, Optional

from node_utils.errors import ExplorationError, RegistrationError
from node_utils.typing import BaseNode, NodeClass, NodeAttr, VisitFn, Context

from .base import BaseExplorer


class NodeVisitor(BaseExplorer[VisitFn, Context]):
    """
    Visitor Generic class:
        visit and view nodes in a tree-like structure of 'NodeClass'

        functions must be pure, taking 'NodeClass' as input and return nothing
    """

    def visit(self, node: BaseNode, context: Optional[Context] = None):
        node_class = node.__class__

        if not isinstance(node, self._node_base_class):
            raise RegistrationError(f"'{node_class.__name__}' is not a '{self.node_class_name}'")

        elif node.__class__ in self._functions.keys():
            self._functions[node_class](node, context)

        elif self._node_base_class in self._functions.keys():
            return self._functions[self._node_base_class](node, context)

        else:
            self._generic_visit(node, context)

    def _generic_visit(self, node: BaseNode, context: Optional[Context] = None):
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

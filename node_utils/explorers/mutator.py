from typing import Dict, List, Optional, Union

from node_utils.errors import ExplorationError, RegistrationError
from node_utils.typing import BaseNode, NodeClass, NodeAttr, MutateFn, Context

from .base import BaseExplorer


class NodeMutator(BaseExplorer[MutateFn, Context]):
    """
    Mutating Visitor Generic class:
        visit and modify nodes in a tree-like structure of 'NodeClass'

        functions must be pure, taking 'NodeClass' as input
        and return it with any necessary modifications
    """

    def update(self, node: BaseNode, context: Optional[Context] = None) -> Optional[BaseNode]:
        node_class = node.__class__

        if not isinstance(node, self._node_base_class):
            raise RegistrationError(f"'{node_class.__name__}' is not a '{self.node_class_name}'")

        elif node.__class__ in self._functions.keys():
            return self._functions[node_class](node, context)

        elif self._node_base_class in self._functions.keys():
            return self._functions[self._node_base_class](node, context)

        else:
            return self._generic_visit(node, context)

    def _generic_visit(
        self, node: BaseNode, context: Optional[Context] = None
    ) -> Union[BaseNode, None]:
        for attr, old_value in node.iter_attributes():
            if isinstance(old_value, list):
                new_values: List[BaseNode] = []
                for old_item in old_value:
                    if isinstance(old_item, self._node_base_class):
                        new_item = self.update(old_item, context)

                        if new_item is None:
                            continue  # pruned node

                        elif isinstance(new_item, self._node_base_class):
                            new_values.append(new_item)

                        else:
                            raise ExplorationError(
                                f"Updated item {new_item} of '{attr}' in "
                                f"{node} is not of type {self.node_class_name}"
                            )

                    else:
                        raise ExplorationError(
                            f"Item {old_item} in '{attr}' of {node} is not of"
                            f" type {self.node_class_name}"
                        )

                setattr(node, attr, new_values)

            elif isinstance(old_value, self._node_base_class):
                new_value = self.update(old_value, context)

                if new_value is None:
                    delattr(node, attr)  # pruned node

                elif isinstance(new_value, self._node_base_class):
                    setattr(node, attr, new_value)

                else:
                    raise ExplorationError(
                        f"Updated '{attr}' {new_value} in {node}"
                        f" is not of type {self.node_class_name}"
                    )

            else:
                raise ExplorationError(
                    f"'{attr}' of {node} is not a list or {self.node_class_name}"
                )

        return node

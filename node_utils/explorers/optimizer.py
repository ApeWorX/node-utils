from typing import List, Optional

from node_utils.errors import ExplorationError
from node_utils.typing import BaseNode, ContextType, OptimizeFn

from .base import BaseExplorer


class NodeOptimizer(BaseExplorer[OptimizeFn]):
    """
    Mutating Visitor Generic class:
        visit and modify nodes in a tree-like structure of 'NodeClass'

        functions must be pure, taking 'NodeClass' as input
        and return it with any necessary modifications
    """

    def update(self, node: BaseNode, context: Optional[ContextType] = None) -> Optional[BaseNode]:
        fn = self._get_registered_function(node) or self.__generic_update
        return fn(node, context)

    def __generic_update(self, node: BaseNode, context: ContextType) -> Optional[BaseNode]:
        for attr, old_value in iter(node):
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

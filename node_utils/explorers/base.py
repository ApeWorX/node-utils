from typing import Dict, Generic

from node_utils.errors import RegistrationError
from node_utils.typing import BaseNode, NodeClass, NodeAttr, FnType, Context


class BaseExplorer(Generic[FnType, Context]):
    def __init__(self, node_base_class: NodeClass):
        self._functions: Dict[NodeClass, FnType] = {}
        self._node_base_class = node_base_class

    @property
    def node_class_name(self):
        return self._node_base_class.__name__

    def register(self, node_class: NodeClass):
        """
        Decorator that allows registering visitor functions
        """

        def register(function: FnType):
            if node_class in self._functions.keys():
                raise RegistrationError(f"'{node_class}' already registered")

            if not issubclass(node_class, self._node_base_class):
                raise RegistrationError(
                    f"'{node_class.__name__}' is not a '{self.node_class_name}'"
                )

            else:
                self._functions[node_class] = function

        return register

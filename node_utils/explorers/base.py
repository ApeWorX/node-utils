from typing import (
    Dict,
    Generic,
    Optional,
)

from node_utils.errors import RegistrationError
from node_utils.typing import (
    BaseNode,
    FnType,
    NodeClass,
)


class BaseExplorer(Generic[FnType]):
    def __init__(self, node_base_class: NodeClass):
        self._functions: Dict[NodeClass, FnType] = {}
        self._node_base_class = node_base_class

    @property
    def node_class_name(self):
        return self._node_base_class.__name__

    def register(self, node_class: NodeClass, allow_override: Optional[bool] = False):
        """
        Decorator that allows registering visitor functions
        """

        def register(function: FnType):
            if node_class in self._functions.keys() and not allow_override:
                raise RegistrationError(f"'{node_class}' already registered")

            if not issubclass(node_class, self._node_base_class):
                raise RegistrationError(
                    f"'{node_class.__name__}' is not a '{self.node_class_name}'"
                )

            else:
                self._functions[node_class] = function

            return function

        return register

    @property
    def registry(self) -> Dict[NodeClass, FnType]:
        return self._functions.copy()

    def _get_registered_function(self, node: BaseNode) -> Optional[FnType]:
        node_class = node.__class__

        if not isinstance(node, self._node_base_class):
            raise RegistrationError(f"'{node_class.__name__}' is not a '{self.node_class_name}'")

        elif node_class in self._functions.keys():
            # User's registered function
            return self._functions[node_class]

        elif self._node_base_class in self._functions.keys():
            # User's registered default
            return self._functions[self._node_base_class]

        else:
            return None

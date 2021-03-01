from inspect import signature
from typing import Dict, Generic, Optional

from node_utils.errors import RegistrationError
from node_utils.typing import BaseNode, FnType, NodeClass


def _handle_no_context(fn: FnType) -> FnType:
    def call(node, context):
        return fn(node)

    return call


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

            sig = signature(function)
            if len(sig.parameters) not in (1, 2):
                raise RegistrationError(
                    f"'{function.__name__}' does not have the right number of args."
                )

            if len(sig.parameters) == 1:
                # Skip providing context, because function doesn't support receiving it
                self._functions[node_class] = _handle_no_context(function)

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
            # User's registered function for specific class takes precedence
            return self._functions[node_class]

        else:
            # See if we have a function registered for one of it's ancestors
            # NOTE: This includes the one registered for `node_base_class`, if available
            for ancestor in node._ancestors():
                if ancestor in self._functions.keys():
                    return self._functions[ancestor]

        return None  # Must handle this with a generic caller, or else it should throw

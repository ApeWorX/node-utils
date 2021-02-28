import dataclasses as _dc
from typing import Generator, List, Tuple, Type, Union

# Use this decorator when defining new node types from BaseNode
node_type = _dc.dataclass

NodeClass = Type["BaseNode"]
NodeAttr = Union[List["BaseNode"], "BaseNode"]


@node_type
class BaseNode:
    def iter_attributes(
        self,
    ) -> Generator[Tuple[str, NodeAttr], None, None]:
        for field in _dc.fields(self):
            value = getattr(self, field.name)
            if isinstance(value, (list, BaseNode)):
                yield field.name, value

    @property
    def type(self):
        return self.__class__.__name__

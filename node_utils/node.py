from typing import Iterator, List, Tuple, Type, Union

from dataclassy import dataclass, values

NodeClass = Type["BaseNode"]
NodeAttr = Union[List["BaseNode"], "BaseNode"]


@dataclass(slots=True)
class BaseNode:
    def __iter__(self) -> Iterator[Tuple[str, NodeAttr]]:
        for name, value in values(self).items():
            if isinstance(value, (list, BaseNode)):
                yield name, value

    @property
    def type(self):
        return self.__class__.__name__

    def _ancestors(self) -> Iterator[Type["BaseNode"]]:
        """
        Return an iterator of all of the classes this one inherits from,
        up to (but not including) the BaseNode class. Iterator must be
        ordered in Method Resolution Order.
        """
        for cls in self.__class__.__mro__:
            if issubclass(cls, BaseNode):
                yield cls

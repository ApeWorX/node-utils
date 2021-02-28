from typing import Generator, List, Tuple, Type, Union

from dataclassy import dataclass, values

NodeClass = Type["BaseNode"]
NodeAttr = Union[List["BaseNode"], "BaseNode"]


@dataclass(slots=True)
class BaseNode:
    def __iter__(self) -> Generator[Tuple[str, NodeAttr], None, None]:
        for name, value in values(self).items():
            if isinstance(value, (list, BaseNode)):
                yield name, value

    @property
    def type(self):
        return self.__class__.__name__

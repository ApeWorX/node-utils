from typing import List

import pytest  # type: ignore

from node_utils import BaseNode


class ASTNode(BaseNode):
    pass


class Constant(ASTNode):
    value: int


class Add(ASTNode):
    lhs: ASTNode
    rhs: ASTNode


class Ls(ASTNode):
    members: List[ASTNode]


def test_type():
    const1 = Constant(1)
    const2 = Constant(2)
    assert const1.type == const2.type == "Constant"

    add = Add(const1, const2)
    assert add.type == "Add"

    ls = Ls([const1, const2, add])
    assert ls.type == "Ls"


def test_iter_attributes():
    # Only attributes that are of type `BaseNode`
    # or `List[BaseNode]` are emitted by the iterator
    const1 = Constant(1)
    const2 = Constant(2)

    assert const1 == Constant(1)
    assert const1.value == 1
    assert const2 == Constant(2)
    assert const2.value == 2

    attr_iter = iter(const1)

    with pytest.raises(StopIteration):
        next(attr_iter)

    attr_iter = iter(const2)

    with pytest.raises(StopIteration):
        next(attr_iter)

    add = Add(const1, const2)

    assert add.lhs == const1 == Constant(1)
    assert add.rhs == const2 == Constant(2)

    attr_iter = iter(add)

    assert next(attr_iter) == ("lhs", add.lhs)
    assert next(attr_iter) == ("rhs", add.rhs)

    with pytest.raises(StopIteration):
        next(attr_iter)

    ls = Ls([const1, const2, add])
    assert ls.members == [const1, const2, add] == [Constant(1), Constant(2), Add(const1, const2)]

    attr_iter = iter(ls)
    assert next(attr_iter) == ("members", ls.members)

    with pytest.raises(StopIteration):
        next(attr_iter)

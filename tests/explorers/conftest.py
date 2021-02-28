import pytest

from node_utils import BaseNode, NodeOptimizer, NodeTransformer, NodeVisitor


@pytest.fixture(scope="session")
def TestNode():
    class TestNode(BaseNode):
        pass

    yield TestNode


@pytest.fixture
def visitor(TestNode):
    class TestVisitor(NodeVisitor):
        pass

    yield TestVisitor(TestNode)


@pytest.fixture
def optimizer(TestNode):
    class TestOptimizer(NodeOptimizer):
        pass

    yield TestOptimizer(TestNode)


@pytest.fixture
def transformer(TestNode):
    class TestTransformer(NodeTransformer):
        pass

    yield TestTransformer(TestNode)

import pytest

from node_utils.errors import ExplorationError, RegistrationError
from node_utils.typing import BaseNode


class OtherNode(BaseNode):
    pass


def test_no_registrations(TestNode, visitor, optimizer, transformer):
    node = TestNode()

    # Default is to do nothing
    assert visitor.visit(node) is None

    # Default is to just return the node
    assert optimizer.update(node) == node

    # Transformer must have a default exploration function defined
    with pytest.raises(ExplorationError):
        transformer.transform(node)


def test_registration_errors(TestNode, visitor):
    # Cannot register an exploration function with the wrong node type
    with pytest.raises(RegistrationError):

        @visitor.register(OtherNode)
        def wrong_node_type(n, c):
            pass

    # Cannot register an exploration function with no `node` input
    with pytest.raises(RegistrationError):

        @visitor.register(TestNode)
        def no_args():
            pass

    # Cannot register an exploration function with more arguments than `node` and `context`
    with pytest.raises(RegistrationError):

        @visitor.register(TestNode)
        def too_many_args(a, b, c):
            pass

    # Okay to register an exploration function that just accepts `node`
    @visitor.register(TestNode)
    def visit_node(n):
        pass

    # Cannot override an exploration function wiht a different one, without opting in
    with pytest.raises(RegistrationError):

        @visitor.register(TestNode)
        def failed_override_visit_node(n, c):
            pass

    # Okay to override a registration with another one
    # NOTE: Here we are overriding to add `context` as an arg, but that's not necessary
    @visitor.register(TestNode, allow_override=True)
    def override_visit_node(n, c):
        pass

    # Can't call our exploration function with a node that isn't a subclass of our registration type
    with pytest.raises(RegistrationError):
        visitor.visit(OtherNode())

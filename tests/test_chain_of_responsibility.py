import pytest
from bolivar_design_patterns.behavioral.chain_of_responsibility.chain import build_checkout_chain
from bolivar_design_patterns.behavioral.chain_of_responsibility.models import CheckoutRequest
from bolivar_design_patterns.behavioral.chain_of_responsibility.handlers import AuthenticationHandler


def request(**changes):
    data = dict(order_id="ORD-1", user_id="user-1", quantity=2,
                available_stock=5, amount_cents=15000, payment_authorized=True)
    data.update(changes)
    return CheckoutRequest(**data)


def test_approves_valid_request():
    assert build_checkout_chain().handle(request()).approved is True


@pytest.mark.parametrize(("overrides", "stage"), [
    ({"user_id": ""}, "authentication"),
    ({"user_id": None}, "authentication"),
    ({"quantity": 6}, "inventory"),
    ({"quantity": 0}, "inventory"),
    ({"payment_authorized": False}, "payment"),
    ({"amount_cents": 0}, "payment"),
])
def test_rejects_at_correct_stage(overrides, stage):
    decision = build_checkout_chain().handle(request(**overrides))
    assert decision.approved is False
    assert decision.stage == stage


def test_requires_explicit_terminal_handler():
    with pytest.raises(ValueError):
        AuthenticationHandler(None)


def test_chain_is_reusable_without_state_leaks():
    chain = build_checkout_chain()
    assert not chain.handle(request(user_id="")).approved
    assert chain.handle(request()).approved

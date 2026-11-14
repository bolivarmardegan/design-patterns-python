"""Composition root: order can be reconfigured without changing handlers."""
from .handlers import (
    Handler, AuthenticationHandler, InventoryHandler, PaymentHandler, CompletedHandler,
)


def build_checkout_chain() -> Handler:
    return AuthenticationHandler(InventoryHandler(PaymentHandler(CompletedHandler())))

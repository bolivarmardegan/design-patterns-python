"""Fail-fast Chain of Responsibility with explicit terminal handler."""
from abc import ABC, abstractmethod
from .models import CheckoutRequest, Decision


class Handler(ABC):
    @abstractmethod
    def handle(self, request: CheckoutRequest) -> Decision:
        """Process or pass the request to the next handler."""


class ForwardingHandler(Handler):
    def __init__(self, next_handler: Handler) -> None:
        if next_handler is None:
            raise ValueError("Every validation chain must have a terminal handler")
        self._next = next_handler

    def _forward(self, request: CheckoutRequest) -> Decision:
        return self._next.handle(request)


class AuthenticationHandler(ForwardingHandler):
    def handle(self, request: CheckoutRequest) -> Decision:
        if not request.user_id or not request.user_id.strip():
            return Decision.reject("authentication", "Authenticated user is required")
        return self._forward(request)


class InventoryHandler(ForwardingHandler):
    def handle(self, request: CheckoutRequest) -> Decision:
        if request.quantity <= 0 or request.available_stock < request.quantity:
            return Decision.reject("inventory", "Insufficient inventory or invalid quantity")
        return self._forward(request)


class PaymentHandler(ForwardingHandler):
    def handle(self, request: CheckoutRequest) -> Decision:
        if request.amount_cents <= 0 or not request.payment_authorized:
            return Decision.reject("payment", "Payment not authorized or invalid amount")
        return self._forward(request)


class CompletedHandler(Handler):
    def handle(self, request: CheckoutRequest) -> Decision:
        return Decision.approve()

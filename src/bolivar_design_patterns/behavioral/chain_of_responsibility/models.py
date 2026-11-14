"""Immutable request and decision objects (purely educational, no payment gateway)."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CheckoutRequest:
    order_id: str
    user_id: str | None
    quantity: int
    available_stock: int
    amount_cents: int
    payment_authorized: bool


@dataclass(frozen=True, slots=True)
class Decision:
    approved: bool
    stage: str
    message: str

    @classmethod
    def reject(cls, stage: str, message: str) -> "Decision":
        return cls(False, stage, message)

    @classmethod
    def approve(cls) -> "Decision":
        return cls(True, "completed", "Checkout approved")

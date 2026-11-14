"""Run with: python -m bolivar_design_patterns.behavioral.chain_of_responsibility.demo"""
from .chain import build_checkout_chain
from .models import CheckoutRequest


def main() -> None:
    chain = build_checkout_chain()
    accepted = CheckoutRequest("ORD-100", "user-1", 2, 5, 15000, True)
    rejected = CheckoutRequest("ORD-101", "user-2", 6, 5, 15000, True)
    print(chain.handle(accepted))
    print(chain.handle(rejected))


if __name__ == "__main__":
    main()

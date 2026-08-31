from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict


# ============================================================
# Payment Models
# ============================================================

class PaymentStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class PaymentRequest:
    amount: float
    currency: str
    customer_id: str


@dataclass
class PaymentResult:
    status: PaymentStatus
    transaction_id: str
    message: str


# ============================================================
# Strategy Interface
# ============================================================

class PaymentStrategy(ABC):
    """
    Common interface for all payment strategies.
    """

    @abstractmethod
    def pay(self, request: PaymentRequest) -> PaymentResult:
        pass


# ============================================================
# Concrete Strategies
# ============================================================

class CreditCardPayment(PaymentStrategy):

    def pay(self, request: PaymentRequest) -> PaymentResult:
        print("Processing credit card payment...")

        transaction_id = "CC-10001"

        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=transaction_id,
            message=(
                f"Credit card payment of "
                f"{request.amount:.2f} {request.currency} successful."
            )
        )


class PayPalPayment(PaymentStrategy):

    def pay(self, request: PaymentRequest) -> PaymentResult:
        print("Processing PayPal payment...")

        transaction_id = "PP-20001"

        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=transaction_id,
            message=(
                f"PayPal payment of "
                f"{request.amount:.2f} {request.currency} successful."
            )
        )


class UPIPayment(PaymentStrategy):

    def pay(self, request: PaymentRequest) -> PaymentResult:
        print("Processing UPI payment...")

        transaction_id = "UPI-30001"

        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=transaction_id,
            message=(
                f"UPI payment of "
                f"{request.amount:.2f} {request.currency} successful."
            )
        )


class BankTransferPayment(PaymentStrategy):

    def pay(self, request: PaymentRequest) -> PaymentResult:
        print("Processing bank transfer...")

        transaction_id = "BANK-40001"

        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=transaction_id,
            message=(
                f"Bank transfer of "
                f"{request.amount:.2f} {request.currency} successful."
            )
        )


# ============================================================
# Payment Processor - Context
# ============================================================

class PaymentProcessor:
    """
    Context class.

    It delegates payment processing to the selected strategy.
    """

    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        """
        Change payment method at runtime.
        """
        self._strategy = strategy

    def process(self, request: PaymentRequest) -> PaymentResult:
        if request.amount <= 0:
            return PaymentResult(
                status=PaymentStatus.FAILED,
                transaction_id="N/A",
                message="Payment amount must be greater than zero."
            )

        if not request.currency:
            return PaymentResult(
                status=PaymentStatus.FAILED,
                transaction_id="N/A",
                message="Currency is required."
            )

        return self._strategy.pay(request)


# ============================================================
# Configurable Strategy Factory
# ============================================================

class PaymentStrategyFactory:

    _strategies: Dict[str, type[PaymentStrategy]] = {
        "card": CreditCardPayment,
        "credit_card": CreditCardPayment,
        "paypal": PayPalPayment,
        "upi": UPIPayment,
        "bank": BankTransferPayment,
        "bank_transfer": BankTransferPayment,
    }

    @classmethod
    def create(cls, payment_method: str) -> PaymentStrategy:
        """
        Create a payment strategy from configuration.
        """

        payment_method = payment_method.lower().strip()

        strategy_class = cls._strategies.get(payment_method)

        if strategy_class is None:
            raise ValueError(
                f"Unsupported payment method: {payment_method}"
            )

        return strategy_class()

    @classmethod
    def register(
        cls,
        name: str,
        strategy_class: type[PaymentStrategy]
    ):
        """
        Dynamically register a new payment strategy.
        """
        if not issubclass(strategy_class, PaymentStrategy):
            raise TypeError(
                "Strategy must inherit from PaymentStrategy"
            )

        cls._strategies[name.lower()] = strategy_class


# ============================================================
# Configuration
# ============================================================

class PaymentConfig:

    def __init__(self, config: Dict[str, str]):
        self.config = config

    def get_strategy(self) -> PaymentStrategy:
        method = self.config.get("payment_method")

        if not method:
            raise ValueError(
                "payment_method is missing from configuration"
            )

        return PaymentStrategyFactory.create(method)


# ============================================================
# Custom Strategy Example
# ============================================================

class CryptocurrencyPayment(PaymentStrategy):

    def pay(self, request: PaymentRequest) -> PaymentResult:
        print("Processing cryptocurrency payment...")

        transaction_id = "CRYPTO-50001"

        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=transaction_id,
            message=(
                f"Cryptocurrency payment of "
                f"{request.amount:.2f} {request.currency} successful."
            )
        )


# Register the new strategy dynamically
PaymentStrategyFactory.register(
    "crypto",
    CryptocurrencyPayment
)


# ============================================================
# Example Usage
# ============================================================

if __name__ == "__main__":

    request = PaymentRequest(
        amount=2500.00,
        currency="INR",
        customer_id="CUSTOMER-101"
    )

    # ----------------------------------------
    # Configuration selects UPI
    # ----------------------------------------

    config = PaymentConfig({
        "payment_method": "upi"
    })

    processor = PaymentProcessor(
        config.get_strategy()
    )

    result = processor.process(request)

    print(result.status.value)
    print(result.transaction_id)
    print(result.message)

    # ----------------------------------------
    # Change strategy at runtime
    # ----------------------------------------

    processor.set_strategy(
        PaymentStrategyFactory.create("paypal")
    )

    result = processor.process(request)

    print("\n" + result.message)

    # ----------------------------------------
    # Use dynamically registered strategy
    # ----------------------------------------

    processor.set_strategy(
        PaymentStrategyFactory.create("crypto")
    )

    result = processor.process(request)

    print("\n" + result.message)

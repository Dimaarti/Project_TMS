from decimal import Decimal

from django.db.models import Sum


class ClientBalanceService:
    @staticmethod
    def build(total_amount, paid_amount):
        raw_balance = total_amount - paid_amount

        return {
            "total_amount": total_amount,
            "paid_amount": paid_amount,
            "debt_amount": max(raw_balance, Decimal("0")),
            "overpayment_amount": abs(min(raw_balance, Decimal("0"))),
        }

    @classmethod
    def calculate(cls, shipment, client_result):
        paid_amount = shipment.client_payments.filter(
            client=client_result.client,
            currency=client_result.calculation_result.final_currency,
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

        return cls.build(
            total_amount=client_result.client_price_cost,
            paid_amount=paid_amount,
        )

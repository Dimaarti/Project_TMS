from collections import defaultdict

from china_calc.finance.calculators.currency_calculator import CurrencyCalculator
from china_calc.finance.calculators.proportional_allocation_calculator import (
    ProportionalAllocationCalculator,
)
from config.model_choices import LogisticCalculationMethod


class ShipmentExpenseCalculator:
    @classmethod
    def calculate(cls, shipment):
        items = list(shipment.items.select_related("client").order_by("pk"))

        if not items:
            raise ValueError("В поставке нет товаров")

        expenses = list(shipment.expenses.select_related("item").order_by("pk"))

        direct_expenses_item = {item.pk: 0 for item in items}

        common_expenses_cost = 0

        for expense in expenses:
            expense_cost = cls.convert_expense(
                expense=expense,
                shipment=shipment,
            )

            if expense.item_id is not None:
                cls.validate_direct_expense(
                    expense=expense,
                    shipment=shipment,
                    direct_expenses_item=direct_expenses_item,
                )
                direct_expenses_item[expense.item_id] += expense_cost
            else:
                common_expenses_cost += expense_cost

        distributed_expense_item = cls.allocate_common_expenses(
            shipment=shipment,
            items=items,
            common_expenses_cost=common_expenses_cost,
        )

        item_allocations = cls.build_item_allocations(
            items=items,
            direct_expenses_item=direct_expenses_item,
            distributed_expenses_item=distributed_expense_item,
        )

        client_allocations = cls.build_client_allocations(
            items=items,
            item_allocations=item_allocations,
        )

        direct_expenses_cost = sum(direct_expenses_item.values(), 0)

        total_expenses_cost = direct_expenses_cost + common_expenses_cost

        return {
            "direct_expenses_cost": direct_expenses_cost,
            "common_expenses_cost": common_expenses_cost,
            "total_expenses_cost": total_expenses_cost,
            "items": item_allocations,
            "clients": client_allocations,
        }

    @staticmethod
    def convert_expense(expense, shipment):
        """
        Переводит расход в итоговую валюту поставки.
        """

        if expense.amount < 0:
            raise ValueError("Сумма расхода не может быть отрицательной")

        return CurrencyCalculator.convert_currency(
            amount=expense.amount,
            purchase_currency=expense.currency,
            final_currency=shipment.settlement_final_currency,
            exchange_rate=shipment.exchange_rate,
            for_client=False,
        )

    @staticmethod
    def validate_direct_expense(expense, shipment, direct_expenses_item):
        """
        Проверяет отношение прямого расхода к товару текущей поставки.
        """

        if expense.item_id not in direct_expenses_item:
            raise ValueError("Товар расхода не принадлежит этой поставке.")


    @classmethod
    def allocate_common_expenses(cls, shipment, items, common_expenses_cost):
        """
        Распределяет общие расходы между товарами (weight or volume)
        """

        if common_expenses_cost == 0:
            return {item.pk: 0 for item in items}

        basis_item = cls.get_basis_item(
            shipment=shipment,
            items=items,
        )

        total_basis = sum(basis_item.values(), 0)

        if total_basis <= 0:
            raise ValueError(
                "Невозможно распределить общие расходы, вес или объем товаров равен 0"
            )

        return ProportionalAllocationCalculator.allocate(
            items=items,
            total_amount=common_expenses_cost,
            basis_item=basis_item,
            total_basis=total_basis,
        )

    @staticmethod
    def get_basis_item(shipment, items):
        """
        Возвращает вес или объем каждого товара.
        """
        calculation_type = shipment.logistic_calculation_type

        if calculation_type == LogisticCalculationMethod.WEIGHT:
            basis_item = {item.pk: item.weight for item in items}

        elif calculation_type == LogisticCalculationMethod.VOLUME:
            basis_item = {item.pk: item.volume for item in items}

        else:
            raise ValueError("Неизвестный способ распределения расходов")

        for item in items:
            basis = basis_item[item.pk]

            if basis is None:
                raise ValueError("У товара не указан вес или объем")

            if basis < 0:
                raise ValueError("Вес или объем товара не может быть отрицательным")

        return basis_item

    @staticmethod
    def build_item_allocations(items, direct_expenses_item, distributed_expenses_item):
        """
        Результат расходов для каждого товара
        """
        result = {}

        for item in items:
            direct_cost = direct_expenses_item.get(item.pk, 0)
            distributed_cost = distributed_expenses_item.get(item.pk, 0)

            result[item.pk] = {
                "item_id": item.pk,
                "client_id": item.client_id,
                "direct_expenses_cost": direct_cost,
                "distributed_expenses_cost": distributed_cost,
                "total_expenses_cost": direct_cost + distributed_cost,
            }

        return result

    @staticmethod
    def build_client_allocations(items, item_allocations):
        """
        Складывает расходы товаров и группирует по клиентам.
        """

        direct_expenses_client = defaultdict(
            lambda: 0,
        )

        distributed_expenses_client = defaultdict(
            lambda: 0,
        )

        for item in items:
            item_allocation = item_allocations[item.pk]

            direct_expenses_client[item.client_id] += item_allocation["direct_expenses_cost"]

            distributed_expenses_client[item.client_id] += item_allocation["distributed_expenses_cost"]

        result = {}

        client_ids = {item.client_id for item in items}

        for client_id in client_ids:
            direct_cost = direct_expenses_client[client_id]
            distributed_cost = distributed_expenses_client[client_id]

            result[client_id] = {
                "client_id": client_id,
                "direct_expenses_cost": direct_cost,
                "distributed_expenses_cost": distributed_cost,
                "total_expenses_cost": direct_cost + distributed_cost,
            }

        return result

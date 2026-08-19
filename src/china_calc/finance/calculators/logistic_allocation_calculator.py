from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal

from china_calc.finance.calculators.logistic_calculator import LogisticCalculator
from china_calc.finance.calculators.proportional_allocation_calculator import (
    ProportionalAllocationCalculator,
)
from config.model_choices import LogisticCalculationMethod


@dataclass(frozen=True)
class ItemLogisticAllocation:
    item_id: int
    client_id: int
    """
    basis - вес или объем конкретного товара
    ratio - доля от 0 до 1
    percent - процент от 0 до 100 
    logistics_cost - распределенная доставка товара
    """
    basis: Decimal
    ratio: Decimal
    percent: Decimal
    logistics_cost: Decimal


@dataclass(frozen=True)
class ClientLogisticAllocation:
    client_id: int
    """
    basis - вес или объем товаров клиента
    ratio - доля клиента от 0 до 1
    percent - процент клиента от 0 до 100 
    logistics_cost - сумма доставки всех товаров клиента
    """
    basis: Decimal
    ratio: Decimal
    percent: Decimal
    logistics_cost: Decimal


@dataclass(frozen=True)
class ShipmentLogisticAllocation:
    logistics_cost: Decimal
    total_basis: Decimal

    items: dict[int, ItemLogisticAllocation]
    clients: dict[int, ClientLogisticAllocation]


class LogisticAllocationCalculator:
    """
    Получает все товары, рассчитывает долю каждого товара, группирует по клиентам.
    """

    @classmethod
    def calculate(cls, shipment, items=None):
        if items is None:
            items = list(shipment.items.select_related("client").order_by("pk"))
        else:
            items = list(items)

        if not items:
            raise ValueError("Отсутствуют товары в поставке ")

        logistics_cost = LogisticCalculator.calculate(
            shipment=shipment,
        )

        basis_item = cls.get_basis_item(
            shipment=shipment,
            items=items,
        )

        total_basis = sum(basis_item.values(), 0)

        if total_basis <= 0:
            raise ValueError("Невозможно распределить логистику")

        amount_item = ProportionalAllocationCalculator.allocate(
            items=items,
            total_amount=logistics_cost,
            basis_item=basis_item,
            total_basis=total_basis,
        )

        item_allocations = cls.build_item_allocations(
            items=items,
            basis_item=basis_item,
            amount_item=amount_item,
            total_basis=total_basis,
        )

        client_allocations = cls.build_client_allocations(
            items=items,
            item_allocations=item_allocations,
            total_basis=total_basis,
        )

        return ShipmentLogisticAllocation(
            logistics_cost=logistics_cost,
            total_basis=total_basis,
            items=item_allocations,
            clients=client_allocations,
        )

    @staticmethod
    def get_basis_item(shipment, items):
        calculation_type = shipment.logistic_calculation_type

        if calculation_type == LogisticCalculationMethod.WEIGHT:
            basis_item = {item.pk: Decimal(item.weight) for item in items}
        elif calculation_type == LogisticCalculationMethod.VOLUME:
            basis_item = {item.pk: Decimal(item.volume) for item in items}
        else:
            raise ValueError("Неизвестный способ распределения")

        for item in items:
            if basis_item[item.pk] < 0:
                raise ValueError("Вес или объем товара не может быть отрицательным")

        return basis_item

    @staticmethod
    def build_item_allocations(items, basis_item, amount_item, total_basis):
        result = {}

        for item in items:
            basis = basis_item[item.pk]
            ratio = basis / total_basis
            percent = ratio * Decimal(100)

            result[item.pk] = ItemLogisticAllocation(
                item_id=item.pk,
                client_id=item.client_id,
                basis=basis,
                ratio=ratio,
                percent=percent,
                logistics_cost=amount_item[item.pk],
            )

        return result

    @staticmethod
    def build_client_allocations(items, item_allocations, total_basis):
        basis_client = defaultdict(lambda: Decimal(0))
        amount_client = defaultdict(lambda: Decimal(0))

        for item in items:
            item_allocation = item_allocations[item.pk]
            basis_client[item.client_id] += item_allocation.basis
            amount_client[item.client_id] += item_allocation.logistics_cost

        result = {}

        for client_id, basis in basis_client.items():
            ratio = basis / total_basis
            percent = ratio * Decimal(100)

            result[client_id] = ClientLogisticAllocation(
                client_id=client_id,
                basis=basis,
                ratio=ratio,
                percent=percent,
                logistics_cost=amount_client[client_id],
            )

        return result

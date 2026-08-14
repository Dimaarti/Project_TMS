class ProportionalAllocationCalculator:
    """
    Распределяет общую сумму между товарами
    пропорционально заданной базе.

    База: вес, объем, количество, стоимость, др. Decimal показатель.
    """

    @staticmethod
    def allocate(items, total_amount, basis_item, total_basis):
        items = list(items)

        if not items:
            return {}

        if total_amount < 0:
            raise ValueError("Распределяемая сумма не может быть отрицательной")

        if total_basis <= 0:
            raise ValueError("Общая база распределения должна быть больше 0")

        allocations = {}
        allocated_amount = 0

        for item in items[:-1]:
            basis = basis_item[item.pk]

            if basis is None:
                raise ValueError("Для товара не указана база распределения")

            if basis < 0:
                raise ValueError(
                    "База распределения товаров не может быть отрицательной"
                )

            amount = total_amount * basis / total_basis

            allocations[item.pk] = amount
            allocated_amount += amount

        last_item = items[-1]
        last_basis = basis_item[last_item.pk]

        if last_basis is None:
            raise ValueError("Для товара не указана база распределения")

        if last_basis < 0:
            raise ValueError("База распределения не может быть отрицательной")

        allocations[last_item.pk] = total_amount - allocated_amount

        return allocations

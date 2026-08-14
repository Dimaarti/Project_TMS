from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font


class ShipmentReportServices:
    def __init__(self, shipment, client):
        self.shipment = shipment
        self.client = client

    def build(self):
        items = list(
            self.shipment.items.filter(client=self.client)
            .select_related("client")
            .order_by("pk")
        )

        if not items:
            raise ValueError("Невозможно скачать отчёт: у клиента нет товаров в этой поставке.")

        calculation_results = (
            self.shipment.calculation_results.filter(is_actual=True)
            .order_by("created_at")
            .first()
        )

        if calculation_results is None:
            raise ValueError("Невозможно скачать отчёт: у поставки нет актуального расчета.")

        client_result = (
            calculation_results.client_results.filter(client=self.client)
            .prefetch_related("item_results__item")
            .first()
        )

        if client_result is None:
            raise ValueError("Невозможно скачать отчёт: для клиента нет результатов расчета.")

        item_results = {
            result.item_id: result
            for result in client_result.item_results.all()
        }

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Отчет клиента"

        sheet.append(
            [
                f"Отчет о поставке {self.shipment.number}",
            ]
        )
        sheet["A1"].font = Font(
            name="Carlito",
            size=16,
            bold=True,
        )

        sheet.append(
            [
                f"Клиент: {self.client.full_name}",
            ]
        )

        sheet["A2"].font = Font(
            name="Carlito",
            size=13,
            bold=True,
        )

        sheet.append([None])

        sheet.append(
            [
                "Маршрут",
                "Статус",
                "Способ расчета",
                "Тариф за 1 кг",
                "Тариф за 1 м3"
            ]
        )

        sheet.append(
            [
                str(self.shipment.route),
                self.shipment.get_status_display(),
                self.shipment.get_logistic_calculation_type_display(),
                self.shipment.tariff_one_kg,
                self.shipment.tariff_one_m3
            ]
        )

        tariff_currency = str(self.shipment.tariff_currency).replace('"', "")

        for column in range(4, 6):
            sheet.cell(
                row=sheet.max_row,
                column=column,
            ).number_format = f'#,##0.00 "{tariff_currency}"'

        sheet.append([None])

        sheet.append(
            [
                "Результат расчета клиента",
                "Сумма",

            ]
        )

        calculation_rows = [
            (
                "Стоимость товара",
                client_result.client_purchase_cost,
                calculation_results.shipment.settlement_final_currency,
            ),
            (
                "Логистика",
                client_result.logistics_cost,
                calculation_results.shipment.settlement_final_currency,
            ),
            (
                "Расходы",
                client_result.expenses_cost,
                calculation_results.shipment.settlement_final_currency,
            ),
            (
                "Комиссия",
                client_result.buyer_commission_cost,
                calculation_results.shipment.settlement_final_currency,
            ),

            (
                "Итого клиенту",
                client_result.client_price_cost,
                calculation_results.shipment.settlement_final_currency,
            )
        ]




        for label, value, currency in calculation_rows:
            sheet.append([label, value, calculation_results.final_currency])

        sheet.append([None])

        sheet.append(
            [
                "Товар",
                "Трек-номер",
                "Количество",
                "Цена",
                "Вес, кг",
                "Объем, м3",
                "Стоимость товара",
                "Логистика",
                "Прямые расходы",
                "Общие расходы",
                "Итого",
                "Ссылка",
            ]
        )

        final_currency = str(calculation_results.final_currency)

        for item in items:
            item_result = item_results.get(item.pk)

            if item_result is None:
                raise ValueError(f"Для товара {item.pk} отсутствует результат расчета")

            sheet.append(
                [
                    item.name,
                    item.tracking_number,
                    item.quantity,
                    item.price,
                    item.weight,
                    item.volume,
                    item_result.client_purchase_cost,
                    item_result.logistics_cost,
                    item_result.direct_expenses_cost,
                    item_result.distributed_expenses_cost,
                    item_result.total_cost,
                    item.product_link
                ]
            )

            price_currency = str(item.price_currency)

            sheet.cell(
                row=sheet.max_row,
                column=4,
            ).number_format = f'#,##0.00 "{price_currency}"'

            for column in range(7, 12):
                sheet.cell(
                    row=sheet.max_row,
                    column=column,
                ).number_format = f'#,##0.00 "{final_currency}"'

            if item.product_link:
                link_cell = sheet.cell(row=sheet.max_row, column=12)
                link_cell.hyperlink = item.product_link
                link_cell.style = "Hyperlink"

        width = {
            "A": 40,
            "B": 18,
            "C": 16,
            "D": 14,
            "E": 14,
            "F": 12,
            "G": 22,
            "H": 16,
            "I": 16,
            "J": 16,
            "K": 16 ,
            "L": 18,
            "M": 18,
        }

        for column, width in width.items():
            sheet.column_dimensions[column].width = width

        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)

        return buffer

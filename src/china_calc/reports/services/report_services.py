from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font


class ShipmentReportServices:
    def __init__(self, shipment):
        self.shipment = shipment

    def build(self):
        items = list(
            self.shipment.item.select_related(
                "product",
                "client",
            )
        )

        if not items:
            raise ValueError(
                "Невозможно скачать отчёт: в поставке нет товаров."
            )
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Отчет"

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

        sheet.append([None])

        sheet.append(
            [
                "Маршрут",
                "Тариф за 1 кг",
                "Тариф за 1 м3",
                "Валюта тарифа",
                "Статус",
                "Вес, кг",
                "Объем, м3",
                "Способ расчета логистики",
            ]
        )

        for cell in sheet[sheet.max_row]:
            cell.font = Font(bold=True)

        sheet.append(
            [
                str(self.shipment.route),
                self.shipment.tariff_one_kg,
                self.shipment.tariff_one_m3,
                self.shipment.tariff_currency,
                self.shipment.status,
                self.shipment.weight,
                self.shipment.volume,
                self.shipment.get_logistic_calculation_type_display(),
            ]
        )

        sheet.append([None])
        sheet.append(["Результат расчета"])
        sheet.cell(
            row=sheet.max_row,
            column=1,
        )

        result = getattr(self.shipment, "calculation_result", None)

        if result:
            calculation_rows = [
                (
                    "Стоимость товара",
                    result.purchase_cost,
                    result.shipment.settlement_final_currency,
                ),
                (
                    "Стоимость товара для клиента",
                    result.client_purchase_cost,
                    result.shipment.settlement_final_currency,
                ),
                (
                    "Логистика",
                    result.logistics_cost,
                    result.shipment.settlement_final_currency,
                ),
                (
                    "Дополнительные услуги",
                    result.additional_services,
                    result.shipment.settlement_final_currency,
                ),
                (
                    "Комиссия байера",
                    result.buyer_commission_cost,
                    result.shipment.settlement_final_currency,
                ),
                (
                    "Себестоимость",
                    result.price_cost,
                    result.shipment.settlement_final_currency,
                ),
                (
                    "Итого для клиента",
                    result.client_price_cost,
                    result.shipment.settlement_final_currency,
                ),
                (
                    "Прибыль",
                    result.profit_cost,
                    result.shipment.settlement_final_currency,
                ),
            ]

            for label, value, currency in calculation_rows:
                sheet.append([label, value, currency])

            sheet.append([None])
            sheet.append(["Товары"])
            sheet.cell(
                row=sheet.max_row,
                column=1,
            ).font = Font(bold=True)

            sheet.append(
                [
                    "Наименование",
                    "Клиент",
                    "Трек-номер",
                    "Количество",
                    "Цена",
                    "Валюта",
                    "Проверка",
                    "Фотоотчет",
                    "Упаковка",
                    "Ссылка",
                ]
            )

            items_header_row = sheet.max_row

            for cell in sheet[items_header_row]:
                cell.font = Font(bold=True)

            for item in self.shipment.item.all():
                if not item:
                    raise ValueError(
                        "Невозможно скачать отчёт: в поставке нет товаров."
                    )
                else:
                    sheet.append(
                        [
                            item.product.name,
                            str(item.client),
                            item.tracking_number,
                            item.quantity,
                            item.price,
                            item.price_currency,
                            item.inspection_cost,
                            item.photo_report_cost,
                            item.packaging_cost,
                            item.product_link or "",
                        ]
                    )

                current_row = sheet.max_row

                price_cell = sheet.cell(
                    row=current_row,
                    column=4,
                )
                price_cell.number_format = "###0.00"

                link_cell = sheet.cell(
                    row=current_row,
                    column=10,
                )

                if item.product_link:
                    link_cell.hyperlink = item.product_link
                    link_cell.style = "Hyperlink"

                sheet.column_dimensions["A"].width = 42

                sheet.column_dimensions["B"].width = 16

                sheet.column_dimensions["C"].width = 14
                sheet.column_dimensions["D"].width = 16
                sheet.column_dimensions["E"].width = 10
                sheet.column_dimensions["F"].width = 10
                sheet.column_dimensions["G"].width = 12
                sheet.column_dimensions["H"].width = 26
                sheet.column_dimensions["I"].width = 10
                sheet.column_dimensions["J"].width = 40

                buffer = BytesIO()
                workbook.save(buffer)
                buffer.seek(0)

                return buffer

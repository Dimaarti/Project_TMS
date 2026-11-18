from datetime import datetime
from io import BytesIO

from django.db.models import Prefetch
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

from china_calc.finance.models import ItemCalculationResult


class ShipmentPackingListServices:
    """Простой упаковочный лист: товары и их трек-номера."""

    def __init__(self, shipment, client=None):
        self.shipment = shipment
        self.client = client

    def build(self):
        calc = self.shipment.calculation_results.filter(is_actual=True).first()
        items_qs = self.shipment.items.select_related("client").order_by(
            "client_id", "pk"
        )
        if self.client is not None:
            items_qs = items_qs.filter(client=self.client)

        if calc is not None:
            items_qs = items_qs.prefetch_related(
                Prefetch(
                    "item_calculation_results",
                    queryset=ItemCalculationResult.objects.filter(
                        client_result__calculation_result=calc
                    ),
                    to_attr="actual_item_results",
                )
            )

        items = list(items_qs)
        if not items:
            raise ValueError("В поставке нет товаров для упаковочного листа")

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Товары и треки"

        thin = Side(style="thin", color="BFBFBF")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)

        # --- заголовок ---
        sheet.append([f"Упаковочный лист · поставка {self.shipment.number}"])
        sheet["A1"].font = Font(name="Carlito", size=15, bold=True)
        sheet.merge_cells("A1:D1")

        subtitle = (
            f"Клиент: {self.client.full_name}"
            if self.client is not None
            else "Клиент: все клиенты поставки"
        )
        sheet.append([subtitle])
        sheet["A2"].font = Font(name="Carlito", size=12, bold=True)
        sheet.merge_cells("A2:D2")

        sheet.append([f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}"])
        sheet.merge_cells("A3:D3")
        sheet.append([None])

        # --- шапка таблицы ---
        headers = ["№", "Товар", "Цена товара, BYN", "Трек-номер", "Кол-во"]
        sheet.append(headers)

        header_row = sheet.max_row
        for col in range(1, 6):
            cell = sheet.cell(row=header_row, column=col)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(fill_type="solid", fgColor="4472C4")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = border

        # --- строки ---
        total_qty = 0
        for idx, item in enumerate(items, start=1):
            item_calc = None
            for r in getattr(item, "actual_item_results", []):
                if self.client is None or r.client_result.client_id == item.client_id:
                    item_calc = r
                    break

            unit_price = (
                (item_calc.purchase_cost / item.quantity)
                if item_calc is not None and item.quantity
                else None
            )

            sheet.append(
                [
                    idx,
                    item.name,
                    unit_price if unit_price is not None else "—",
                    item.tracking_number or "—",
                    item.quantity,
                ]
            )
            row = sheet.max_row
            total_qty += item.quantity

            for col in range(1, 6):
                cell = sheet.cell(row=row, column=col)
                cell.border = border
                cell.alignment = Alignment(
                    vertical="center",
                    horizontal="center" if col in (1, 5) else "left",
                    wrap_text=(col == 2),
                )

            # выделяем трек-номер
            track_cell = sheet.cell(row=row, column=4)
            if item.tracking_number:
                track_cell.font = Font(bold=True, color="1F4E79")
            else:
                track_cell.font = Font(color="999999", italic=True)

        # --- итог ---
        sheet.append(["", "ИТОГО", "", "", total_qty])
        total_row = sheet.max_row
        for col in range(1, 6):
            cell = sheet.cell(row=total_row, column=col)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(fill_type="solid", fgColor="FFF2CC")
            cell.border = border
            cell.alignment = Alignment(horizontal="center" if col in (1, 5) else "left")

        # --- ширины ---
        sheet.column_dimensions["A"].width = 6
        sheet.column_dimensions["B"].width = 55
        sheet.column_dimensions["C"].width = 20
        sheet.column_dimensions["D"].width = 30
        sheet.column_dimensions["E"].width = 10

        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)
        return buffer

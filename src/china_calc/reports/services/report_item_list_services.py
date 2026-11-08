from datetime import datetime
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side


class ShipmentPackingListServices:
    """Простой упаковочный лист: товары и их трек-номера."""

    def __init__(self, shipment, client=None):
        self.shipment = shipment
        self.client = client

    def build(self):
        items_qs = self.shipment.items.select_related("client").order_by(
            "client_id", "pk"
        )
        if self.client is not None:
            items_qs = items_qs.filter(client=self.client)

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
        headers = ["№", "Товар", "Трек-номер", "Кол-во"]
        sheet.append(headers)

        header_row = sheet.max_row
        for col in range(1, 5):
            cell = sheet.cell(row=header_row, column=col)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(fill_type="solid", fgColor="4472C4")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = border

        # --- строки ---
        total_qty = 0
        for idx, item in enumerate(items, start=1):
            sheet.append(
                [
                    idx,
                    item.name,
                    item.tracking_number or "—",
                    item.quantity,
                ]
            )
            row = sheet.max_row
            total_qty += item.quantity

            for col in range(1, 5):
                cell = sheet.cell(row=row, column=col)
                cell.border = border
                cell.alignment = Alignment(
                    vertical="center",
                    horizontal="center" if col in (1, 4) else "left",
                    wrap_text=(col == 2),
                )

            # выделяем трек-номер
            track_cell = sheet.cell(row=row, column=3)
            if item.tracking_number:
                track_cell.font = Font(bold=True, color="1F4E79")
            else:
                track_cell.font = Font(color="999999", italic=True)

        # --- итог ---
        sheet.append(["", "ИТОГО", "", total_qty])
        total_row = sheet.max_row
        for col in range(1, 5):
            cell = sheet.cell(row=total_row, column=col)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(fill_type="solid", fgColor="FFF2CC")
            cell.border = border
            cell.alignment = Alignment(horizontal="center" if col in (1, 4) else "left")

        # --- ширины ---
        sheet.column_dimensions["A"].width = 6
        sheet.column_dimensions["B"].width = 55
        sheet.column_dimensions["C"].width = 28
        sheet.column_dimensions["D"].width = 10

        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)
        return buffer

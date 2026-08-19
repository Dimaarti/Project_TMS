from django.contrib import admin

from china_calc.finance.models.calculation_result import CalculationResult
from china_calc.finance.models.client_calculation_result import ClientCalculationResult
from china_calc.finance.models.exchange_rate import ExchangeRate
from china_calc.finance.models.item_calculation_result import ItemCalculationResult

admin.site.register(ExchangeRate)
admin.site.register(CalculationResult)
admin.site.register(ClientCalculationResult)
admin.site.register(ItemCalculationResult)

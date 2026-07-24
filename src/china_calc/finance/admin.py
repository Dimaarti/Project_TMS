from django.contrib import admin

from china_calc.finance.models.calculation_result import CalculationResult
from china_calc.finance.models.exchange_rate import ExchangeRate

admin.site.register(ExchangeRate)
admin.site.register(CalculationResult)

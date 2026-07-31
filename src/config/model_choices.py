from django.db import models


class Currency(models.TextChoices):
    CNY = "CNY", "Китайский юань"
    RUB = "RUB", "Российский Рубль"
    USD = "USD", "Американский доллар"
    BYN = "BYN", "Белорусский рубль"


class SettlementFinalCurrency(models.TextChoices):
    RUB = "RUB", "Российский Рубль"
    BYN = "BYN", "Белорусский рубль"


class ExpenseType(models.TextChoices):
    TRANSPORT = "transport", "Международная доставка"
    TC = "transport_company", "Доставка транспортной компанией"
    INSURANCE = "insurance", "Страхование"
    LOADING = "loading", "Загрузка"
    UNLOADING = "unloading", "Отгрузка"
    OTHER = "other", "Прочее"


class LogisticCalculationMethod(models.TextChoices):
    WEIGHT = "weight", "По весу"
    VOLUME = "volume", "По объему"


class TransportType(models.TextChoices):
    AIR = "air", "Авиационный"
    AUTO = "auto", "Автомобильный"
    SEA = "sea", "Морской"
    RAIL = "rail", "Железнодорожный"

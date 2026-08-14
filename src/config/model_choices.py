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
    TRANSPORT_COMPANY = "transport_company", "Доставка транспортной компанией"
    INSURANCE = "insurance", "Страхование"
    LOADING = "loading", "Погрузка"
    UNLOADING = "unloading", "Разгрузка"
    INSPECTION = "inspection", "Проверка товара"
    PHOTO_REPORT = "photo_report", "Фотоотчет"
    ITEM_PACKAGING = "item_packaging", "Упаковка товара"
    SHIPMENT_PACKAGING = "shipments_packaging", "Упаковка посылки"
    CUSTOMS = "customs", "Таможенные расходы"
    STORAGE = "storage", "Хранение"
    OTHER = "other", "Прочее"


class LogisticCalculationMethod(models.TextChoices):
    WEIGHT = "weight", "По весу"
    VOLUME = "volume", "По объему"


class TransportType(models.TextChoices):
    AIR = "air", "Авиационный"
    AUTO = "auto", "Автомобильный"
    SEA = "sea", "Морской"
    RAIL = "rail", "Железнодорожный"


class ExpenseDistributionMethod(models.TextChoices):
    LOGISTIC = (
        "logistic",
        "Как основная логистика",
    )
    WEIGHT = (
        "weight",
        "По весу",
    )
    VOLUME = (
        "volume",
        "По объёму",
    )
    PURCHASE_PRICE = (
        "purchase_price",
        "По стоимости товаров",
    )
    EQUAL_ITEMS = (
        "equal_items",
        "Поровну между товарами",
    )


class ShipmentStatus(models.TextChoices):
    EDITE = "edite", "Редактируется"
    CALCULATED = "calculated", "Рассчитана"
    CLOSED = "closed", "Закрыта"

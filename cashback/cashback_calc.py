from cashback.models import Cashback
from products.models import ProductType

class CashbackCalc:
    def __init__(self, cashback: Cashback) -> None:
        self.cashback = cashback

    def calc(self) -> float:
        cashback = 0
        for product in self.cashback.products.all():
            cashback_percent = ProductType.objects.filter(type=product.type).first().cashback_percent
            cashback += cashback_percent * product.value * product.qty
        return cashback


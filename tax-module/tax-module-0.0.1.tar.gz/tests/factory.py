from tax_module.models import PricingType, Price, TaxableItem


def create_taxable_item(price: Price = None, region: str = None, item_type: str = None):
    class FakeTaxableItem(TaxableItem):
        @property
        def price(self):
            return price or create_price()

        @property
        def region(self):
            return region or "NCR"

        @property
        def item_type(self):
            return item_type or "SERVICE"

    return FakeTaxableItem()


def create_price(amount: int = None, pricing_type: PricingType = None):
    return Price(
        amount=amount or 100, pricing_type=pricing_type or PricingType.TAX_INCLUSIVE
    )

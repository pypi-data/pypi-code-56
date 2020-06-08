from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List


class PricingType(Enum):
    TAX_INCLUSIVE = "TAX_INCLUSIVE"
    TAX_EXCLUSIVE = "TAX_EXCLUSIVE"


@dataclass
class Price:
    amount: int
    pricing_type: PricingType

    @property
    def is_tax_inclusive(self):
        return self.pricing_type == PricingType.TAX_INCLUSIVE


@dataclass
class Tax:
    tax_percentage: int
    tax_type: str


class AppliedTax:
    def __init__(self, tax: Tax, price: Price, sum_of_taxes: int):
        tax_exclusive_amount = (
            (price.amount * 100 / (100 + sum_of_taxes))
            if price.is_tax_inclusive
            else price.amount
        )
        self.tax = tax
        self.amount = round((tax_exclusive_amount * self.tax.tax_percentage) / 100, 2)


class TaxableItem(ABC):
    @property
    @abstractmethod
    def price(self) -> Price:
        pass

    @property
    @abstractmethod
    def region(self) -> str:
        pass

    @property
    @abstractmethod
    def item_type(self) -> str:
        pass


@dataclass
class TaxedItem(ABC):
    taxes: List[AppliedTax]


class TaxableItemType(Enum):
    GOOD = "GOOD"
    SERVICE = "SERVICE"
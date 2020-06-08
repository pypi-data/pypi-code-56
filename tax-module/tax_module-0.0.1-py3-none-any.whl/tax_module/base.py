from typing import List

from tax_module.models import AppliedTax, TaxableItem
from tax_module.errors import NoTaxRuleFoundError


class TaxModule:
    def __init__(self, rule_book: dict):
        self._rule_book = rule_book  # It is a dictionary which tells which tax_type applies to which zone

    def get_taxes_for_taxable_item(self, taxable_item: TaxableItem) -> List[AppliedTax]:
        try:
            taxes_to_apply = self._rule_book[taxable_item.region][
                taxable_item.item_type
            ]
        except KeyError:
            raise self._mk_exc(
                region=taxable_item.region, item_type=taxable_item.item_type
            )
        sum_of_taxes = sum(tax.tax_percentage for tax in taxes_to_apply)
        return [
            AppliedTax(tax=tax, price=taxable_item.price, sum_of_taxes=sum_of_taxes)
            for tax in taxes_to_apply
        ]

    def _mk_exc(self, region: str, item_type: str) -> NoTaxRuleFoundError:
        return NoTaxRuleFoundError(
            f"""
        No Tax Rule Found for
        Region: {region}
        ItemType:{item_type}
        """
        )


def get_tax_module(rule_book):
    return TaxModule(rule_book=rule_book)

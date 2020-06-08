import pytest

from tax_module.base import TaxModule
from tax_module.models import PricingType, Tax
from tax_module.errors import NoTaxRuleFoundError
from tests.factory import create_taxable_item, create_price


def test_tax_module_gives_single_tax_for_taxable_item():
    fake_rule_book = {
        "MY_REGION": {"TAXABLE_ITEM_TYPE": [Tax(tax_percentage=10, tax_type="MY_TAX")]}
    }

    tax_module = TaxModule(rule_book=fake_rule_book)
    taxable_item = create_taxable_item(
        region="MY_REGION", item_type="TAXABLE_ITEM_TYPE"
    )
    taxes = tax_module.get_taxes_for_taxable_item(taxable_item)

    assert len(taxes) == 1
    assert taxes[0].tax.tax_percentage == 10
    assert taxes[0].tax.tax_type == "MY_TAX"
    assert taxes[0].amount == 9.09


def test_tax_module_gives_multiple_taxes_for_taxable_item():
    fake_rule_book = {
        "MY_REGION": {
            "TAXABLE_ITEM_TYPE": [
                Tax(tax_percentage=10, tax_type="MY_TAX"),
                Tax(tax_percentage=11, tax_type="MY_TAX1"),
            ]
        }
    }

    tax_module = TaxModule(rule_book=fake_rule_book)
    taxable_item = create_taxable_item(
        region="MY_REGION", item_type="TAXABLE_ITEM_TYPE"
    )
    taxes = tax_module.get_taxes_for_taxable_item(taxable_item)

    assert len(taxes) == 2
    assert taxes[0].tax.tax_percentage == 10
    assert taxes[0].tax.tax_type == "MY_TAX"
    assert taxes[0].amount == 8.26
    assert taxes[1].tax.tax_percentage == 11
    assert taxes[1].tax.tax_type == "MY_TAX1"
    assert taxes[1].amount == 9.09


def test_tax_module_raises_exception_incase_no_rule_exists():
    fake_rule_book = {
        "MY_REGION": {
            "OTHER_TAXABLE_ITEM_TYPE": [Tax(tax_percentage=10, tax_type="MY_TAX")]
        }
    }

    tax_module = TaxModule(rule_book=fake_rule_book)
    taxable_item = create_taxable_item(
        region="MY_REGION", item_type="TAXABLE_ITEM_TYPE"
    )
    with pytest.raises(NoTaxRuleFoundError):
        tax_module.get_taxes_for_taxable_item(taxable_item)


def test_tax_module_for_price_exclusive_taxable_item():
    fake_rule_book = {
        "MY_REGION": {"TAXABLE_ITEM_TYPE": [Tax(tax_percentage=10, tax_type="MY_TAX")]}
    }

    tax_module = TaxModule(rule_book=fake_rule_book)
    taxable_item = create_taxable_item(
        region="MY_REGION",
        item_type="TAXABLE_ITEM_TYPE",
        price=create_price(amount=100, pricing_type=PricingType.TAX_EXCLUSIVE),
    )
    taxes = tax_module.get_taxes_for_taxable_item(taxable_item)

    assert len(taxes) == 1
    assert taxes[0].tax.tax_percentage == 10
    assert taxes[0].tax.tax_type == "MY_TAX"
    assert taxes[0].amount == 10.0

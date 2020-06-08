from typing import Dict, List

from tax_module.models import Tax

CGST_PERCENTAGE_FOR_SERVICE = 6
SGST_PERCENTAGE_FOR_SERVICE = 6
IGST_PERCENTAGE_FOR_SERVICE = 12

INDIAN_TAX_RULE_BOOK: Dict[str, Dict[str, List[Tax]]] = {
    "MAHARASHTRA": {
        "SERVICE": [
            Tax(tax_type="CGST", tax_percentage=CGST_PERCENTAGE_FOR_SERVICE),
            Tax(tax_type="SGST", tax_percentage=SGST_PERCENTAGE_FOR_SERVICE),
        ]
    },
    "NCR": {
        "SERVICE": [Tax(tax_type="IGST", tax_percentage=IGST_PERCENTAGE_FOR_SERVICE)]
    },
    "TAMIL NADU": {
        "SERVICE": [
            Tax(tax_type="CGST", tax_percentage=CGST_PERCENTAGE_FOR_SERVICE),
            Tax(tax_type="SGST", tax_percentage=SGST_PERCENTAGE_FOR_SERVICE),
        ]
    },
    "TELANGANA": {
        "SERVICE": [
            Tax(tax_type="CGST", tax_percentage=CGST_PERCENTAGE_FOR_SERVICE),
            Tax(tax_type="SGST", tax_percentage=SGST_PERCENTAGE_FOR_SERVICE),
        ]
    },
    "WEST BENGAL": {
        "SERVICE": [
            Tax(tax_type="CGST", tax_percentage=CGST_PERCENTAGE_FOR_SERVICE),
            Tax(tax_type="SGST", tax_percentage=SGST_PERCENTAGE_FOR_SERVICE),
        ]
    },
}

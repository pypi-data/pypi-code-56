from typing import Any, Dict

from jeffy.validator import ValidationError, Validator

import jsonschema


class JsonSchemeValidator(Validator):
    """JSON scheme validator."""

    def __init__(self, scheme: Dict):
        """
        Initialize JsonSchemeValidator.

        Parameters
        ----------
        scheme: Dict
        """
        self.scheme = scheme

    def validate(self, data: Any) -> None:
        """
        Validate the data by JSON scheme.

        Parameters
        ----------
        data: Any

        Raises
        ------
        jeffy.validator.ValidationError
        """
        try:
            jsonschema.validate(data, self.scheme)
        except jsonschema.ValidationError as e:
            raise ValidationError(e)

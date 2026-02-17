import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class ProductionYearValidator:
    min_year = 1900

    def __call__(self, value):
        max_year = datetime.datetime.now().year
        if not self.min_year <= value <= max_year:
            raise ValidationError(f'Car production year must be from {self.min_year} to {max_year}.')



class PlateValidator(RegexValidator):
    regex = r'^[ETYOPAHKXCBM]{1,2}\d{4}[ETYOPAHKXCBM]{1,2}$'
    message = 'Invalid plate number. Use Bulgarian format (e.g., CB1234AB).'

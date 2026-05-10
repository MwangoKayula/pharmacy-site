import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class CyrillicValidator:
    def __init__(self, message=None):
        self.message = message or "Only Cyrillic letters, digits, hyphens, and spaces are allowed."

    def __call__(self, value):
        # Pattern: allows Cyrillic (upper/lower), digits, hyphen, space
        if not re.fullmatch(r'[А-Яа-яЁё0-9\-\s]+', value):
            raise ValidationError(self.message, code='invalid_cyrillic')
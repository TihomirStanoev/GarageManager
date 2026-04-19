from django.core.validators import RegexValidator


class PhoneNumberValidator(RegexValidator):
    regex = r'^\+359\d{9}$'
    message = 'Invalid phone number. Use Bulgarian format (e.g., +359888123456).'
import re
from django.core.exceptions import ValidationError


def validate_uzbekistan_phone(value):
    """
    Validate Uzbekistan phone number format
    Expected format: +998XXXXXXXXX or 998XXXXXXXXX (13 digits total including country code)
    """
    # Remove any spaces, hyphens, or parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', value)
    
    # Check if it starts with +998 or 998
    if cleaned.startswith('+998'):
        cleaned = cleaned[1:]  # Remove the + sign
    
    if not cleaned.startswith('998'):
        raise ValidationError('Phone number must start with +998 or 998')
    
    if len(cleaned) != 12:  # 998 + 9 digits
        raise ValidationError('Uzbekistan phone number must be 12 digits long (including country code 998)')
    
    if not cleaned.isdigit():
        raise ValidationError('Phone number must contain only digits')
    
    # Check if the number follows Uzbek mobile format (after 998, should start with specific codes)
    mobile_prefixes = ['90', '91', '93', '94', '95', '97', '98', '99', '33', '71', '77', '88']
    operator_code = cleaned[3:5]
    
    if operator_code not in mobile_prefixes:
        raise ValidationError('Invalid Uzbekistan mobile operator code')


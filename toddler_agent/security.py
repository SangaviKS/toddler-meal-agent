"""
Security module for Toddler Meal Concierge Agent.
Validates and sanitizes all user inputs before processing.
"""

import re
from typing import Optional


def validate_age_months(age_months: int) -> tuple[bool, str]:
    """
    Validates that age in months is within a reasonable toddler range.
    """
    if not isinstance(age_months, int):
        return False, "Age must be a whole number of months."
    if age_months < 6:
        return False, "This agent supports children 6 months and older."
    if age_months > 60:
        return False, "This agent supports children up to 60 months (5 years)."
    return True, "valid"


def sanitize_text_input(text: str, field_name: str) -> tuple[bool, str]:
    """
    Sanitizes free text inputs to prevent prompt injection attacks.
    Removes special characters and limits length.
    """
    if not isinstance(text, str):
        return False, f"{field_name} must be a text value."

    # Check length
    if len(text) > 200:
        return False, f"{field_name} is too long. Please keep it under 200 characters."

    # Detect prompt injection attempts
    injection_patterns = [
        r"ignore previous instructions",
        r"forget your instructions",
        r"you are now",
        r"pretend you are",
        r"system prompt",
        r"<script>",
        r"DROP TABLE",
    ]
    text_lower = text.lower()
    for pattern in injection_patterns:
        if re.search(pattern, text_lower):
            return False, f"Invalid input detected in {field_name}."

    # Sanitize — allow only safe characters
    sanitized = re.sub(r"[^\w\s,.\-']", "", text)
    return True, sanitized


def validate_allergies(allergies: list[str]) -> tuple[bool, list[str]]:
    """
    Validates and sanitizes a list of allergy strings.
    """
    if not isinstance(allergies, list):
        return False, ["Allergies must be provided as a list."]

    if len(allergies) > 20:
        return False, ["Too many allergies listed. Please limit to 20."]

    sanitized = []
    for allergy in allergies:
        valid, result = sanitize_text_input(allergy, "allergy")
        if not valid:
            return False, [result]
        sanitized.append(result.lower().strip())

    return True, sanitized


def validate_and_sanitize_request(
    age_months: Optional[int] = None,
    allergies: Optional[list[str]] = None,
    food_item: Optional[str] = None,
) -> tuple[bool, dict]:
    """
    Master validation function for all incoming requests.
    Returns (is_valid, sanitized_data_or_error_message).
    """
    result = {}

    if age_months is not None:
        valid, message = validate_age_months(age_months)
        if not valid:
            return False, {"error": message}
        result["age_months"] = age_months

    if allergies is not None:
        valid, sanitized = validate_allergies(allergies)
        if not valid:
            return False, {"error": sanitized[0]}
        result["allergies"] = sanitized

    if food_item is not None:
        valid, sanitized = sanitize_text_input(food_item, "food item")
        if not valid:
            return False, {"error": sanitized}
        result["food_item"] = sanitized

    return True, result
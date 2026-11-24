
import re

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "qwerty",
    "admin",
    "letmein",
    "welcome",
    "iloveyou",
}


def analyze_password(password: str) -> dict:
    """
    Analyze password strength and return a score, level,
    criteria and improvement suggestions.
    """

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        return {
            "score": 0,
            "level": "Very Weak",
            "criteria": {},
            "suggestions": ["Enter a password to analyze."]
        }

    criteria = {
        "length": len(password) >= 12,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digits": bool(re.search(r"\d", password)),
        "symbols": bool(re.search(r"[^A-Za-z0-9]", password)),
    }

    score = sum(criteria.values()) * 20
    suggestions = []

    if len(password) < 12:
        suggestions.append("Use at least 12 characters.")

    if not criteria["uppercase"]:
        suggestions.append("Add uppercase letters.")

    if not criteria["lowercase"]:
        suggestions.append("Add lowercase letters.")

    if not criteria["digits"]:
        suggestions.append("Include numbers.")

    if not criteria["symbols"]:
        suggestions.append("Include special characters.")

    if password.lower() in COMMON_PASSWORDS:
        score = 0
        suggestions.append("Avoid common passwords.")

    if score < 40:
        level = "Weak"
    elif score < 80:
        level = "Medium"
    else:
        level = "Strong"

    return {
        "score": score,
        "level": level,
        "criteria": criteria,
        "suggestions": suggestions
    }

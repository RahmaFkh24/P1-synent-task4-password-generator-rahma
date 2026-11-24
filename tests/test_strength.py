
import pytest

from src.strength import analyze_password


def test_empty_password():
    result = analyze_password("")
    assert result["score"] == 0
    assert result["level"] == "Very Weak"


def test_strong_password():
    result = analyze_password("SecurePass@2026")
    assert result["score"] == 100
    assert result["level"] == "Strong"


def test_weak_password():
    result = analyze_password("abc")
    assert result["level"] == "Weak"


def test_missing_uppercase():
    result = analyze_password("securepass@2026")
    assert result["criteria"]["uppercase"] is False
    assert "Add uppercase letters." in result["suggestions"]


def test_missing_digits():
    result = analyze_password("SecurePassword@")
    assert result["criteria"]["digits"] is False


def test_missing_symbols():
    result = analyze_password("SecurePassword2026")
    assert result["criteria"]["symbols"] is False


def test_common_password():
    result = analyze_password("password123")
    assert result["score"] == 0
    assert "Avoid common passwords." in result["suggestions"]


def test_invalid_input():
    with pytest.raises(TypeError):
        analyze_password(123456)


def test_all_criteria():
    result = analyze_password("MySecure@Password2026")
    assert all(result["criteria"].values())

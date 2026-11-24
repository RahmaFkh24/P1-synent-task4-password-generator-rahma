
import string
import pytest

from src.generator import generate_password


def test_default_password_length():
    password = generate_password()
    assert len(password) == 16


def test_custom_password_length():
    password = generate_password(length=24)
    assert len(password) == 24


def test_all_character_categories():
    password = generate_password(length=20)

    assert any(c in string.ascii_uppercase for c in password)
    assert any(c in string.ascii_lowercase for c in password)
    assert any(c in string.digits for c in password)
    assert any(c in string.punctuation for c in password)


def test_password_without_symbols():
    password = generate_password(
        length=16,
        use_symbols=False
    )

    assert all(c not in string.punctuation for c in password)


def test_password_without_numbers():
    password = generate_password(
        length=16,
        use_digits=False
    )

    assert all(c not in string.digits for c in password)


def test_no_category_selected():
    with pytest.raises(ValueError):
        generate_password(
            use_uppercase=False,
            use_lowercase=False,
            use_digits=False,
            use_symbols=False
        )


def test_invalid_password_length():
    with pytest.raises(ValueError):
        generate_password(length=5)


def test_password_length_above_limit():
    with pytest.raises(ValueError):
        generate_password(length=100)


def test_non_integer_length():
    with pytest.raises(ValueError):
        generate_password(length="16")

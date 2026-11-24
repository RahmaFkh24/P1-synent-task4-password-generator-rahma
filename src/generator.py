
import secrets
import string

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 64


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True
) -> str:
    """
    Generate a cryptographically secure random password.

    Args:
        length: Desired password length (8–64).
        use_uppercase: Include uppercase letters.
        use_lowercase: Include lowercase letters.
        use_digits: Include numeric characters.
        use_symbols: Include special characters.

    Returns:
        A randomly generated password.

    Raises:
        ValueError: If the parameters are invalid.
    """

    if type(length) is not int:
        raise ValueError("Password length must be an integer.")

    if not MIN_PASSWORD_LENGTH <= length <= MAX_PASSWORD_LENGTH:
        raise ValueError(
            f"Password length must be between "
            f"{MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH}."
        )

    options = (
        use_uppercase,
        use_lowercase,
        use_digits,
        use_symbols
    )

    if any(type(option) is not bool for option in options):
        raise ValueError("Character options must be boolean values.")

    character_categories = []

    if use_uppercase:
        character_categories.append(string.ascii_uppercase)

    if use_lowercase:
        character_categories.append(string.ascii_lowercase)

    if use_digits:
        character_categories.append(string.digits)

    if use_symbols:
        character_categories.append(string.punctuation)

    if not character_categories:
        raise ValueError("Select at least one character category.")

    if length < len(character_categories):
        raise ValueError(
            "Password length is too short for the selected categories."
        )

    all_characters = "".join(character_categories)

    password_characters = [
        secrets.choice(category)
        for category in character_categories
    ]

    password_characters.extend(
        secrets.choice(all_characters)
        for _ in range(length - len(password_characters))
    )

    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)

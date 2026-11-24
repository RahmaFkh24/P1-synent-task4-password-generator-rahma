
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
        length: Desired password length (8-64).
        use_uppercase: Include uppercase letters.
        use_lowercase: Include lowercase letters.
        use_digits: Include numeric characters.
        use_symbols: Include special characters.

    Returns:
        A securely generated password.

    Raises:
        ValueError: If the configuration is invalid.
    """

    # Step 1: Validate password length
    if type(length) is not int:
        raise ValueError("Password length must be an integer.")

    if not MIN_PASSWORD_LENGTH <= length <= MAX_PASSWORD_LENGTH:
        raise ValueError(
            f"Password length must be between "
            f"{MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH}."
        )

    # Step 2: Define available character categories
    character_categories = []

    if use_uppercase:
        character_categories.append(string.ascii_uppercase)

    if use_lowercase:
        character_categories.append(string.ascii_lowercase)

    if use_digits:
        character_categories.append(string.digits)

    if use_symbols:
        character_categories.append(string.punctuation)

    # Step 3: Ensure at least one category is selected
    if not character_categories:
        raise ValueError("Select at least one character category.")

    # Step 4: Check that the length can accommodate
    # at least one character from every selected category
    if length < len(character_categories):
        raise ValueError(
            "Password length is too short for the selected categories."
        )

    # Step 5: Combine all selected character sets
    all_characters = "".join(character_categories)

    # Step 6: Guarantee one character from each category
    password_characters = [
        secrets.choice(category)
        for category in character_categories
    ]

    # Step 7: Fill the remaining password positions
    remaining_length = length - len(password_characters)

    for _ in range(remaining_length):
        password_characters.append(secrets.choice(all_characters))

    # Step 8: Securely shuffle the characters
    secure_random = secrets.SystemRandom()
    secure_random.shuffle(password_characters)

    # Step 9: Return the final password
    return "".join(password_characters)

from collections.abc import Callable
from hashlib import sha256


def calculate_sha256_digest(value: str) -> str:
    if len(value) == 0:
        return value
    return sha256(value.encode("utf-8")).hexdigest()


def hash_email_preserve_domain(email: str, hashing_func: Callable[[str], str] = calculate_sha256_digest) -> str:
    """Hashes an email address."""
    elems = email.split("@")
    if len(elems) != 2:
        raise ValueError("attempted hash of a bad email")

    name, domain = elems
    hashed_name = hashing_func(name.lower())
    hashed_email = f"{hashed_name}@{domain}"

    return hashed_email
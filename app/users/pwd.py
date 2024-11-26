import bcrypt


class PwdManagerMixin:
    """Mixin class providing password hashing and verification methods."""

    def gen_hash(self, password: str) -> bytes:
        """Generates a hash for the provided plaintext password."""

        salt = bcrypt.gensalt()
        pwd_bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    def verify_hash(self, raw_password: str, hashed_password: bytes) -> bool:
        """Verifies that a plain text password matches with the given hashed password."""

        return bcrypt.checkpw(
            password=raw_password.encode(),
            hashed_password=hashed_password,
        )

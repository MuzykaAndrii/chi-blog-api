from datetime import UTC, datetime, timedelta
import jwt
from .exceptions import AuthenticationExpired, NotAuthenticated


class AuthTokenManager:
    """Handles JWT creation and decoding for user authentication."""

    def __init__(self, alg: str, secret: str, exp_delta: timedelta) -> None:
        self._alg = alg
        self._secret = secret
        self._exp_delta = exp_delta

    def create_token(self, id: int) -> str:
        """Generates a JWT for a user, embedding the expiration and user ID."""

        return jwt.encode(
            payload={
                "exp": self._get_exp_timestamp(),
                "sub": str(id),
            },
            key=self._secret,
            algorithm=self._alg,
        )

    def read_token(self, token: str) -> str:
        """Decodes and verifies the JWT, returning the user ID."""

        try:
            decoded = jwt.decode(token, self._secret, algorithms=[self._alg])
            return decoded["sub"]

        except jwt.ExpiredSignatureError:
            raise AuthenticationExpired

        except jwt.InvalidSignatureError:
            # TODO: log hack attempt
            raise NotAuthenticated

        except jwt.InvalidTokenError:
            raise NotAuthenticated

    def _get_exp_timestamp(self) -> float:
        """Retrieves the expiration timestamp for the token."""

        exp_datetime = datetime.now(UTC) + self._exp_delta
        return exp_datetime.timestamp()

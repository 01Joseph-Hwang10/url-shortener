import os
from src.common.error import throw


class Config:
    """Config class for the application.

    This class contains the configuration for the application.
    """

    @property
    def env(self) -> str:
        """Environment name."""
        return os.environ.get("ENV", "development")

    @property
    def server_name(self) -> str:
        """Server name. Includes domain and port (if any)."""
        return os.environ.get("SERVER_NAME", None) or throw(
            ValueError("SERVER_NAME is not set")
        )

class Config:
    """Config class for the application.

    This class contains the configuration for the application.
    """

    @property
    def server_name(self) -> str:
        """Server name. Includes domain and port (if any)."""
        return "localhost:8000"

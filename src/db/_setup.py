from .model import URL


def setup_db_for_development(truncate: bool = False) -> None:
    """Setup the database for development.

    It creates tables if they do not exist.

    Args:
        truncate: Truncate tables if items exist. Default is False.
    """
    # Create tables if they do not exist
    URL.create_table(safe=True)

    if truncate:
        # Truncate tables
        URL.truncate_table(restart_identity=True, cascade=True)

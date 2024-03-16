import os
import uvicorn
from dotenv import load_dotenv
from src.db import register_database, setup_db_for_development
from src.app import bootstrap
from src.app.container import Container

# Load environment variables if not in production
if os.environ.get("ENV", "development") == "development":
    load_dotenv()

# Create dependency container
container = Container()
container.init_resources()
register_database(container.db())
container.wire()

# Create FastAPI app
app = bootstrap()
app.container = container

if __name__ == "__main__":
    # Set up database for development
    setup_db_for_development()

    # Run the app
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

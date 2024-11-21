import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the values from the environment variables
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_port = os.getenv('POSTGRES_PORT')
postgres_db = os.getenv('POSTGRES_DB')
SECRET_KEY = os.getenv('SECRET_KEY', "'i=.zBs[XfAu.E4N|yl98,q'h5#XJd")
SENTRY_DSN = os.getenv('SENTRY_DSN', "'https://examplePublicKey@o0.ingest.sentry.io/0")

# Construct the DATABASE_URL dynamically
DATABASE_URL = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

# DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5444/bookings"


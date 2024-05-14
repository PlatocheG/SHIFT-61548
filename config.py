#uvicorn settings
API_HOST = "0.0.0.0"
API_PORT = 8000
API_LOG_LEVEL = "info"

#DB settings:
DB_URL = "sqlite+pysqlite:///./database.db"

# JWT:
JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_ALGORITHM = "HS256"
JWT_EXP_TIME_SEC = 20

#pytest
TEST_API_URL = "http://localhost:8000"
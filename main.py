import uvicorn
from fastapi import FastAPI

from auth.auth_routes import router as auth_router
from config import API_HOST, API_PORT, API_LOG_LEVEL

from user.user_routes import router as user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, log_level=API_LOG_LEVEL)

import uvicorn
from fastapi import FastAPI

from auth.auth_routes import router as auth_router
from user.user_routes import router as user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

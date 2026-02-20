from fastapi import FastAPI, status, HTTPException
from .database import Base, engine
from .routers import register_users, login_user, admin_user


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/health', status_code=status.HTTP_200_OK)
def health():
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="API is healthy and running correctly.",
        headers={"Iron_Ready Healthcheack": "healthy"}
    )


app.include_router(register_users.router)
app.include_router(login_user.router)
app.include_router(admin_user.router)
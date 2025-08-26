from fastapi import FastAPI
from .auth import router as auth_router
from .divination import router as divination_router
from .stripe_integration import router as stripe_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth")
app.include_router(divination_router, prefix="/api/divine")
app.include_router(stripe_router, prefix="/api/payment")

@app.get("/")
async def root():
    return {"message": "Welcome to uranAI backend!"}

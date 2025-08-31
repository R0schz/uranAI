from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.auth import router as auth_router
from backend.divination import router as divination_router
from backend.stripe_integration import router as stripe_router

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発環境では全てのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # 全てのHTTPメソッドを許可
    allow_headers=["*"],  # 全てのヘッダーを許可
)

# ルーターの登録
app.include_router(auth_router)
app.include_router(divination_router)
app.include_router(stripe_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to uranAI backend!"}

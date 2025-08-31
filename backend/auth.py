import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from supabase import create_client, Client
from dotenv import load_dotenv

# .env.localファイルを明示的に読み込む
load_dotenv(dotenv_path='uranai/.env.local')

router = APIRouter()

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
# バックエンドでは強力なservice_roleキーを使います
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# "tokenUrl"はダミーです。トークンはフロントがSupabaseから直接取得するため。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/current-user")
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    ヘッダーからJWTを取得し、Supabaseに検証を依頼する。
    有効なユーザーであればユーザー情報を返し、無効であれば例外を発生させる。
    """
    try:
        # 受け取ったJWTを使ってユーザー情報を取得
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
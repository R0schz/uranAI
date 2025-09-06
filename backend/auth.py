import jwt
import os
from datetime import datetime, timezone
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

# .env.localファイルを読み込む（backendディレクトリから実行するため、相対パスに変更）
load_dotenv(dotenv_path='.env.local')

# SupabaseのJWT_SECRETを使用
JWT_SECRET = os.getenv("JWT_SECRET")

security = HTTPBearer()

async def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    SupabaseのJWTトークンを検証し、ユーザーIDを返す
    """
    try:
        token = credentials.credentials
        print(f"Received token: {token[:20]}...")  # トークンの最初の20文字を表示
        print(f"JWT_SECRET exists: {bool(JWT_SECRET)}")
        print(f"JWT_SECRET length: {len(JWT_SECRET) if JWT_SECRET else 0}")
        
        # JWTトークンをデコード（Supabaseの形式に合わせる）
        # audienceチェックを無効化し、より柔軟な検証を行う
        payload = jwt.decode(
            token, 
            JWT_SECRET, 
            algorithms=["HS256"],
            options={
                "verify_signature": True,
                "verify_aud": False,  # audienceチェックを無効化
                "verify_iss": False,  # issuerチェックも無効化（必要に応じて）
            }
        )
        
        print(f"JWT payload: {payload}")  # ペイロードの内容を表示
        
        # SupabaseのJWTトークンからユーザーIDを取得
        user_id = payload.get("sub")
        if not user_id:
            print("User ID not found in token payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )
        
        print(f"Extracted user ID: {user_id}")
        
        # トークンの有効期限をチェック（標準的なPythonのdatetimeを使用）
        exp = payload.get("exp")
        if exp:
            current_timestamp = int(datetime.now(timezone.utc).timestamp())
            if current_timestamp > exp:
                print("Token has expired")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired"
                )
        
        return user_id
        
    except jwt.ExpiredSignatureError:
        print("JWT ExpiredSignatureError")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        print(f"JWT validation error: {e}")
        print(f"JWT validation error type: {type(e)}")
        print(f"JWT validation error details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        print(f"Authentication error: {e}")
        print(f"Authentication error type: {type(e)}")
        print(f"Authentication error details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )

def get_current_user_id(user_id: str = Depends(verify_jwt_token)):
    """
    現在のユーザーIDを取得する依存関数
    """
    return user_id
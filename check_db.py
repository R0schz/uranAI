from backend.database import engine, Base
from sqlalchemy import text

def check_and_create_database():
    try:
        print("データベース接続をテスト中...")
        with engine.connect() as conn:
            print("データベース接続成功！")
            
            # データベース内のテーブル一覧を確認
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            print("存在するテーブル:", tables)
            
            if not tables:
                print("テーブルが存在しません。テーブルを作成します...")
                # テーブルを作成
                Base.metadata.create_all(bind=engine)
                print("テーブルを作成しました")
                
                # 作成後のテーブル一覧を確認
                result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
                tables = [row[0] for row in result]
                print("作成後のテーブル:", tables)
                
                if 'users' in tables:
                    # usersテーブルの構造を確認
                    result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' ORDER BY ordinal_position"))
                    print("\nusersテーブルの構造:")
                    for row in result:
                        print(f"  {row[0]}: {row[1]}")
                
                if 'people' in tables:
                    # peopleテーブルの構造を確認
                    result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'people' ORDER BY ordinal_position"))
                    print("\npeopleテーブルの構造:")
                    for row in result:
                        print(f"  {row[0]}: {row[1]}")
            else:
                print("既存のテーブルを確認中...")
                if 'users' in tables:
                    # usersテーブルの構造を確認
                    result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' ORDER BY ordinal_position"))
                    print("\nusersテーブルの構造:")
                    for row in result:
                        print(f"  {row[0]}: {row[1]}")
                
                if 'people' in tables:
                    # peopleテーブルの構造を確認
                    result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'people' ORDER BY ordinal_position"))
                    print("\npeopleテーブルの構造:")
                    for row in result:
                        print(f"  {row[0]}: {row[1]}")
                        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_and_create_database()

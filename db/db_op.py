import os
import psycopg2
from typing import List, Dict

# =========================
# DB 連線設定
# =========================
def get_connection():
    # 從環境變數抓 Internal Database URL
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("Missing DATABASE_URL environment variable")
    
    # psycopg2.connect 可以直接使用 URL
    return psycopg2.connect(DATABASE_URL)

# =========================
# 1. 插入一筆訊息
# =========================
def set_user_message_history(user_name: str, role: str, message: str):
    print("INSERT MESSAGE : (", user_name, ") ", role, " : ", message)
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO messages (name, role, message) VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (user_name, role, message))
    conn.commit()
    cursor.close()
    conn.close()

# =========================
# 2. 查詢某使用者所有訊息
# 回傳 List[dict[str, str]]
# =========================
def get_user_message_history(user_name: str) -> List[Dict[str, str]]:
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    SELECT name, role, message FROM messages WHERE name = %s ORDER BY id
    """
    cursor.execute(sql, (user_name,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # 確保只回傳 string -> string
    result: List[Dict[str, str]] = []
    for r in rows:
        result.append({
            "name": str(r[0]),
            "role": str(r[1]),
            "message": str(r[2])
        })
    return result

# =========================
# 3. 刪除某使用者所有訊息
# =========================
def clear_user_message_history(user_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM messages WHERE name = %s"
    cursor.execute(sql, (user_name,))
    conn.commit()
    cursor.close()
    conn.close()
import mysql.connector

# =========================
# 1. 連線 MySQL
# =========================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1141compute",
    database="1141_compute_db"
)

cursor = conn.cursor(dictionary=True)

# =========================
# 2. 新增三筆資料
# =========================
insert_sql = """
INSERT INTO messages (name, role, message)
VALUES (%s, %s, %s)
"""

data = [
    ("Alice", "user", "Hello"),
    ("Bob", "assistant", "Hi Alice"),
    ("Alice", "user", "How are you?")
]

cursor.executemany(insert_sql, data)
conn.commit()

print("=== 已新增三筆資料 ===")

# =========================
# 3. 印出最新一筆資料
# =========================
cursor.execute("""
SELECT * FROM messages
ORDER BY id DESC
LIMIT 1
""")

latest = cursor.fetchone()
print("\n=== 最新一筆資料 ===")
print(latest)

# =========================
# 4. 用 name 尋找所有符合的資料（會印出兩筆）
# =========================
cursor.execute("""
SELECT * FROM messages
WHERE name = %s
ORDER BY id
""", ("Alice",))

alice_messages = cursor.fetchall()

print("\n=== name = 'Alice' 的所有資料 ===")
for msg in alice_messages:
    print(msg)

# =========================
# 5. 刪除其中一筆（刪除第一筆 Alice）
# =========================
delete_id = alice_messages[0]["id"]

cursor.execute("""
DELETE FROM messages
WHERE id = %s
""", (delete_id,))

conn.commit()

print(f"\n=== 已刪除 id = {delete_id} 的資料 ===")

# =========================
# 收尾
# =========================
cursor.close()
conn.close()
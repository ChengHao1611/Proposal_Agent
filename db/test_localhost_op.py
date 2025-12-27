# test_op.py
from db_op import (
    set_user_message_history,
    get_user_message_history,
    clear_user_message_history
)

def main():
    user = "Bob"

    print("=== 清空舊資料 ===")
    clear_user_message_history(user)

    print("=== 插入三筆資料 ===")
    set_user_message_history(user, "user", "Hello")
    set_user_message_history(user, "user", "How are you?")
    set_user_message_history(user, "assistant", "I'm fine")

    print("=== 查詢 Alice 的所有訊息（應該有 3 筆） ===")
    history = get_user_message_history(user)

    for msg in history:
        print(msg)

    print(f"總筆數: {len(history)}")

    print("=== 刪除 Alice 的所有訊息 ===")
    clear_user_message_history(user)

    print("=== 再次查詢（應該是空的） ===")
    history = get_user_message_history(user)
    print(history)
    print(f"總筆數: {len(history)}")


if __name__ == "__main__":
    main()
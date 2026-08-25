import sqlite3

DB_PATH = "construction.db"

def add_url_column():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Добавляем колонку url, если её нет
    try:
        cursor.execute("ALTER TABLE normatives ADD COLUMN url TEXT")
        print("✅ Добавлено поле url")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("⏩ Поле url уже существует")
        else:
            print(f"❌ Ошибка: {e}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_url_column()
import sqlite3

DB_PATH = "construction.db"

def check_urls():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Проверяем, есть ли поле url
    cursor.execute("PRAGMA table_info(normatives)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'url' not in columns:
        print("❌ Поле 'url' отсутствует в таблице!")
        print("Запустите сначала: python add_url_column.py")
        return
    
    # Считаем, у скольких документов есть url
    cursor.execute("SELECT COUNT(*) FROM normatives WHERE url IS NOT NULL AND url != ''")
    with_url = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM normatives")
    total = cursor.fetchone()[0]
    
    print(f"📊 Всего документов: {total}")
    print(f"🔗 Документов с ссылками: {with_url}")
    print(f"❌ Без ссылок: {total - with_url}")
    
    # Покажем документы без ссылок
    if with_url < total:
        print("\n📋 Документы без ссылок (первые 10):")
        cursor.execute("SELECT number, title FROM normatives WHERE url IS NULL OR url = '' LIMIT 10")
        rows = cursor.fetchall()
        for row in rows:
            print(f"  - {row[0]}: {row[1][:50]}...")
    
    conn.close()

if __name__ == "__main__":
    check_urls()

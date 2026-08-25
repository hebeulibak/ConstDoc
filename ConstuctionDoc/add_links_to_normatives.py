import sqlite3

DB_PATH = "construction.db"

# Ссылки на полные версии документов
URLS = {
    "48.13330.2019": "https://docs.cntd.ru/document/1200167849",
    "28.13330.2017": "https://docs.cntd.ru/document/1200146883",
    "63.13330.2018": "https://docs.cntd.ru/document/1200163530",
    "12.3.046-91": "https://docs.cntd.ru/document/901710469",
    "134.13330.2022": "https://docs.cntd.ru/document/1200176586",
    # Добавьте другие по мере необходимости
}

def add_urls():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Добавляем колонку url, если её нет
    try:
        cursor.execute("ALTER TABLE normatives ADD COLUMN url TEXT")
        print("✅ Добавлено поле url")
    except sqlite3.OperationalError:
        print("⏩ Поле url уже существует")
    
    updated = 0
    for number, url in URLS.items():
        cursor.execute("UPDATE normatives SET url = ? WHERE number = ?", (url, number))
        if cursor.rowcount > 0:
            updated += cursor.rowcount
            print(f"  ✅ {number} -> {url}")
    
    conn.commit()
    conn.close()
    print(f"\n✅ Обновлено {updated} нормативов")

if __name__ == "__main__":
    add_urls()

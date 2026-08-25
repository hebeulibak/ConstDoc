import sqlite3

DB_PATH = "construction.db"

# Ссылки на полные версии документов
URLS = {
    "1.1130.2020": "https://docs.cntd.ru/document/1200174506",
    "48.13330.2019": "https://docs.cntd.ru/document/1200167849",
    "28.13330.2017": "https://docs.cntd.ru/document/1200146883",
    "63.13330.2018": "https://docs.cntd.ru/document/1200163530",
    "12.3.046-91": "https://docs.cntd.ru/document/901710469",
    "134.13330.2022": "https://docs.cntd.ru/document/1200176586",
}

def add_urls():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Сначала проверим, какие документы есть в БД
    cursor.execute("SELECT number FROM normatives")
    existing_numbers = [row[0] for row in cursor.fetchall()]
    print(f"📊 Документов в БД: {len(existing_numbers)}")
    
    updated = 0
    for number, url in URLS.items():
        if number in existing_numbers:
            cursor.execute("UPDATE normatives SET url = ? WHERE number = ?", (url, number))
            updated += cursor.rowcount
            print(f"  ✅ {number} -> {url}")
        else:
            print(f"  ⚠️ {number} - не найден в БД")
    
    conn.commit()
    conn.close()
    print(f"\n✅ Обновлено {updated} нормативов")

if __name__ == "__main__":
    print("=" * 50)
    print("ДОБАВЛЕНИЕ ССЫЛОК НА ПОЛНЫЕ ТЕКСТЫ")
    print("=" * 50)
    add_urls()
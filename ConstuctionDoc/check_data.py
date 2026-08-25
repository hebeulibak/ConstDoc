import sqlite3

DB_PATH = "construction.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Смотрим все записи в журнале
cursor.execute("SELECT id, date, work_type, work_description, location, responsible_person FROM general_journal")
rows = cursor.fetchall()

print("=" * 50)
print("Записи в журнале:")
print("=" * 50)
for row in rows:
    print(f"ID: {row[0]}")
    print(f"  Дата: {row[1]}")
    print(f"  Тип работ: {row[2]}")
    print(f"  Описание: {row[3]}")
    print(f"  Место: {row[4]}")
    print(f"  Ответственный: {row[5]}")
    print("-" * 30)

conn.close()
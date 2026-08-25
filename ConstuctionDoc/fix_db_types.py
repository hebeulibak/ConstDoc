import sqlite3

DB_PATH = "construction.db"

def fix_database_types():
    """Исправление типов нормативов в БД"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Смотрим какие типы есть в БД
    cursor.execute("SELECT DISTINCT doc_type FROM normatives")
    types = cursor.fetchall()
    print("Типы в БД до исправления:")
    for t in types:
        print(f"  - {t[0]}")
    
    # Заменяем некорректные типы
    cursor.execute("UPDATE normatives SET doc_type = 'Документ' WHERE doc_type = 'Постановление'")
    print(f"Обновлено 'Постановление' -> 'Документ': {cursor.rowcount} записей")
    
    cursor.execute("UPDATE normatives SET doc_type = 'Документ' WHERE doc_type = 'Приказ'")
    print(f"Обновлено 'Приказ' -> 'Документ': {cursor.rowcount} записей")
    
    cursor.execute("UPDATE normatives SET doc_type = 'СП' WHERE doc_type = 'Свод правил'")
    print(f"Обновлено 'Свод правил' -> 'СП': {cursor.rowcount} записей")
    
    cursor.execute("UPDATE normatives SET doc_type = 'СанПиН' WHERE doc_type = 'СанПин'")
    print(f"Обновлено 'СанПин' -> 'СанПиН': {cursor.rowcount} записей")
    
    conn.commit()
    
    # Проверяем результат
    cursor.execute("SELECT DISTINCT doc_type FROM normatives")
    types = cursor.fetchall()
    print("\nТипы в БД после исправления:")
    for t in types:
        print(f"  - {t[0]}")
    
    conn.close()
    print("\n✅ База данных исправлена!")

if __name__ == '__main__':
    fix_database_types()
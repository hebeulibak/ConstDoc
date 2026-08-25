import sqlite3
import json
import os

DB_PATH = "construction.db"
JSON_FOLDER = "rnaJSON"  # Ваша папка

def import_all_json():
    # Полный путь к папке
    full_path = os.path.join('.', JSON_FOLDER)
    
    if not os.path.exists(full_path):
        print(f"❌ Папка '{full_path}' не найдена!")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    json_files = [f for f in os.listdir(full_path) if f.endswith('.json')]
    print(f"📁 Папка: {JSON_FOLDER}")
    print(f"📄 Найдено JSON-файлов: {len(json_files)}")
    print("=" * 50)
    
    count = 0
    errors = 0
    
    for filename in json_files:
        filepath = os.path.join(full_path, filename)
        print(f"\n📖 Обработка: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                
                # Извлекаем данные
                doc_number = data.get('number', '')
                if not doc_number:
                    # Пробуем извлечь номер из filename
                    doc_number = filename.replace('.json', '').replace('_', ' ')
                
                doc_type = data.get('document_type', data.get('type', 'Документ'))
                doc_title = data.get('full_name', data.get('title', filename.replace('.json', '')))
                doc_full_title = data.get('full_name', doc_title)
                status = data.get('status', 'Действует')
                actual_date = data.get('date_issue', data.get('actual_date', ''))
                if actual_date and len(actual_date) > 10:
                    actual_date = actual_date[:10]
                
                # Категория/теги
                tags = data.get('category', '')
                
                # Собираем содержание из страниц
                content = doc_full_title + "\n\n"
                pages = data.get('pages', [])
                page_count = 0
                for page in pages:
                    page_content = page.get('page_content', '')
                    if page_content:
                        content += page_content + "\n\n"
                        page_count += 1
                
                if page_count == 0:
                    content = doc_full_title + "\n\nСодержание документа не найдено."
                
                print(f"  📄 Номер: {doc_number}")
                print(f"  📑 Тип: {doc_type}")
                print(f"  📃 Страниц с текстом: {page_count}")
                
                # Проверяем, существует ли уже
                cursor.execute("SELECT id FROM normatives WHERE number = ?", (doc_number,))
                existing = cursor.fetchone()
                
                if existing:
                    # Обновляем существующий
                    cursor.execute('''UPDATE normatives 
                        SET doc_type = ?, title = ?, full_title = ?, 
                            status = ?, actual_date = ?, tags = ?, content = ?
                        WHERE number = ?''',
                        (doc_type[:20], doc_title[:200], doc_full_title[:500],
                         status[:50], actual_date[:10], tags[:200], content[:5000], doc_number))
                    print(f"  ✅ Обновлён: {doc_number}")
                else:
                    # Добавляем новый
                    cursor.execute('''INSERT INTO normatives 
                        (doc_type, number, title, full_title, status, actual_date, tags, content, is_favorite)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (doc_type[:20], doc_number[:50], doc_title[:200], 
                         doc_full_title[:500], status[:50], actual_date[:10], 
                         tags[:200], content[:5000], 0))
                    print(f"  ✅ Добавлен: {doc_number}")
                
                count += 1
                
            except json.JSONDecodeError as e:
                print(f"  ❌ Ошибка JSON: {e}")
                errors += 1
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
                errors += 1
    
    conn.commit()
    conn.close()
    print("\n" + "=" * 50)
    print(f"🎉 Результат:")
    print(f"   ✅ Обработано: {count}")
    print(f"   ❌ Ошибок: {errors}")
    print(f"   📁 Всего файлов: {len(json_files)}")

def check_database():
    """Проверяет, сколько нормативов в БД"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM normatives")
    count = cursor.fetchone()[0]
    conn.close()
    print(f"\n📊 В базе данных сейчас: {count} нормативов")

if __name__ == "__main__":
    print("=" * 50)
    print("ИМПОРТ НОРМАТИВОВ ИЗ ПАПКИ rnaJSON")
    print("=" * 50)
    print()
    
    # Показываем текущее состояние
    check_database()
    
    print("\nНачинаем импорт...")
    print()
    
    import_all_json()
    
    print("\n" + "=" * 50)
    check_database()
    print("\n✅ Готово! Перезапустите приложение: python app.py")
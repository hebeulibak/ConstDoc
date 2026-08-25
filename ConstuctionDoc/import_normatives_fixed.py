import sqlite3
import json
import os

DB_PATH = "construction.db"

# Укажите имя вашей подпапки с JSON-файлами
# Например: JSON_FOLDER = "downloaded_files" или JSON_FOLDER = "json_data"
JSON_FOLDER = "название_вашей_папки"  # ← ИЗМЕНИТЕ ЭТО!

def import_all_json():
    # Полный путь к папке
    full_path = os.path.join('.', JSON_FOLDER)
    
    if not os.path.exists(full_path):
        print(f"❌ Папка '{full_path}' не найдена!")
        print("\nВот все папки в текущей директории:")
        for item in os.listdir('.'):
            if os.path.isdir(item):
                print(f"  - {item}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    json_files = [f for f in os.listdir(full_path) if f.endswith('.json')]
    print(f"Найдено JSON-файлов в папке '{JSON_FOLDER}': {len(json_files)}")
    
    count = 0
    
    for filename in json_files:
        filepath = os.path.join(full_path, filename)
        print(f"\nОбработка: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                
                # Извлекаем данные
                doc_number = data.get('number', '')
                if not doc_number:
                    doc_number = filename.replace('.json', '').replace('_', ' ')
                
                doc_type = data.get('document_type', data.get('type', 'Документ'))
                doc_title = data.get('full_name', data.get('title', filename.replace('.json', '')))
                doc_full_title = data.get('full_name', doc_title)
                status = data.get('status', 'Действует')
                actual_date = data.get('date_issue', data.get('actual_date', ''))
                if actual_date and len(actual_date) > 10:
                    actual_date = actual_date[:10]
                
                # Собираем содержание
                content = doc_full_title + "\n\n"
                pages = data.get('pages', [])
                for page in pages[:10]:
                    page_content = page.get('page_content', '')
                    if page_content:
                        content += page_content + "\n\n"
                
                if not content or len(content) < 100:
                    content = doc_full_title + "\n\nСодержание документа не загружено полностью."
                
                # Проверяем, существует ли уже
                cursor.execute("SELECT id FROM normatives WHERE number = ?", (doc_number,))
                existing = cursor.fetchone()
                
                if existing:
                    cursor.execute('''UPDATE normatives 
                        SET doc_type = ?, title = ?, full_title = ?, 
                            status = ?, actual_date = ?, content = ?
                        WHERE number = ?''',
                        (doc_type[:20], doc_title[:200], doc_full_title[:500],
                         status[:50], actual_date[:10], content[:5000], doc_number))
                    print(f"  ✅ Обновлён: {doc_number}")
                else:
                    cursor.execute('''INSERT INTO normatives 
                        (doc_type, number, title, full_title, status, actual_date, content, is_favorite)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                        (doc_type[:20], doc_number[:50], doc_title[:200], 
                         doc_full_title[:500], status[:50], actual_date[:10], content[:5000], 0))
                    print(f"  ✅ Добавлен: {doc_number}")
                
                count += 1
                
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
    
    conn.commit()
    conn.close()
    print(f"\n{'='*40}")
    print(f"Обработано файлов: {count}")

if __name__ == "__main__":
    print("Импорт нормативов из JSON...")
    print("=" * 40)
    
    # Показываем все папки для выбора
    print("\nДоступные папки в текущей директории:")
    folders = [f for f in os.listdir('.') if os.path.isdir(f)]
    for i, folder in enumerate(folders, 1):
        print(f"  {i}. {folder}")
    
    print("\nВведите номер папки или название:")
    choice = input("> ")
    
    if choice.isdigit() and 1 <= int(choice) <= len(folders):
        JSON_FOLDER = folders[int(choice)-1]
    else:
        JSON_FOLDER = choice
    
    print(f"\nВыбрана папка: {JSON_FOLDER}")
    import_all_json()
    print("\nГотово! Запустите: python app.py")

import sqlite3
import json
import os

DB_PATH = "construction.db"
JSON_FOLDER = "." # Текущая папка, где лежат JSON-файлы. Можете заменить на полный путь

def get_full_text_from_json(filepath):
    """Извлекает полный текст документа из JSON файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Начинаем с полного названия документа
        full_text = data.get('full_name', '')
        
        # Добавляем текст со всех страниц
        pages = data.get('pages', [])
        for page in pages:
            page_content = page.get('page_content', '')
            if page_content:
                full_text += f"\n\n--- Страница {page.get('page', '?')} ---\n{page_content}"
                
        # Если по какой-то причине текст не извлёкся
        if not full_text or len(full_text) < 50:
             # Добавим краткое описание, если оно есть
             full_text = data.get('scope', '') or data.get('full_name', 'Содержание не найдено')

        return full_text.strip()
    except Exception as e:
        print(f"  ⚠️ Ошибка при чтении файла {os.path.basename(filepath)}: {e}")
        return None

def update_database():
    """Основная функция для обновления БД."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Найдём все JSON-файлы в папке
    json_files = [f for f in os.listdir(JSON_FOLDER) if f.endswith('.json')]
    print(f"🔍 Найдено JSON-файлов: {len(json_files)}")
    
    updated_count = 0
    error_count = 0

    for filename in json_files:
        filepath = os.path.join(JSON_FOLDER, filename)
        print(f"📄 Обработка: {filename}...")
        
        full_content = get_full_text_from_json(filepath)
        
        if not full_content:
            error_count += 1
            continue
            
        # Пытаемся найти документ в БД по номеру, который указан в JSON
        # Сначала прочитаем номер из файла
        with open(filepath, 'r', encoding='utf-8') as f:
            temp_data = json.load(f)
            doc_number = temp_data.get('number')
            
        if not doc_number:
            print(f"  ⚠️ Не удалось определить номер документа. Пропускаем.")
            error_count += 1
            continue
            
        # Обновляем запись в базе данных
        cursor.execute("UPDATE normatives SET content = ? WHERE number = ?", (full_content, doc_number))
        
        if cursor.rowcount > 0:
            print(f"  ✅ Обновлён: {doc_number}")
            updated_count += 1
        else:
            # Если документа с таким номером нет в БД, добавим его
            print(f"  ➕ Документ {doc_number} не найден в БД. Добавляем...")
            doc_type = temp_data.get('type', 'Документ')[:20]
            doc_title = temp_data.get('filename', '').replace('.pdf', '')
            full_title = temp_data.get('full_name', '')
            status = temp_data.get('status', 'Действует')
            actual_date = temp_data.get('date_issue', '')[:10]
            category = temp_data.get('category', '')
            
            cursor.execute('''INSERT INTO normatives 
                (doc_type, number, title, full_title, status, actual_date, tags, content, is_favorite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (doc_type, doc_number, doc_title[:200], full_title[:500], status, actual_date, category, full_content, 0))
            updated_count += 1

    conn.commit()
    conn.close()
    print("\n" + "="*40)
    print(f"✅ Готово! Обновлено/добавлено: {updated_count} нормативов")
    print(f"⚠️ С ошибками: {error_count}")

if __name__ == "__main__":
    update_database()

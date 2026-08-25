import sqlite3
import json
import os
from database import DB_PATH

def import_all_normatives():
    """Импорт всех нормативов из JSON файлов"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Проверяем, сколько уже есть
    cursor.execute("SELECT COUNT(*) FROM normatives")
    current_count = cursor.fetchone()[0]
    print(f"Текущее количество нормативов: {current_count}")
    
    if current_count > 300:
        print("Нормативов уже достаточно, пропускаем")
        conn.close()
        return
    
    # Очищаем таблицу (если нужно обновить)
    # cursor.execute("DELETE FROM normatives")
    
    # Папка с JSON файлами
    json_folder = "rnaJSON"
    
    if not os.path.exists(json_folder):
        print(f"Папка {json_folder} не найдена!")
        return
    
    files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
    print(f"Найдено JSON файлов: {len(files)}")
    
    added = 0
    errors = 0
    
    for filename in files:
        filepath = os.path.join(json_folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Извлекаем данные из JSON
            doc_type = "Документ"
            if "ГОСТ" in filename:
                doc_type = "ГОСТ"
            elif "СНиП" in filename:
                doc_type = "СНиП"
            elif "СП" in filename or "Свод правил" in filename:
                doc_type = "СП"
            elif "СанПиН" in filename or "СанПин" in filename:
                doc_type = "СанПиН"
            elif "Закон" in filename or "Федеральный закон" in filename:
                doc_type = "Закон"
            elif "Постановление" in filename:
                doc_type = "Постановление"
            
            # Извлекаем номер и название
            number = filename.replace('.json', '')
            title = data.get('title', number) if isinstance(data, dict) else number
            
            # Получаем содержимое
            content = ""
            if isinstance(data, dict):
                content = data.get('content', data.get('text', ''))
                if not content and 'description' in data:
                    content = data['description']
            elif isinstance(data, str):
                content = data
            
            # Вставляем в БД
            cursor.execute('''
                INSERT INTO normatives 
                (doc_type, number, title, full_title, status, actual_date, tags, content, is_favorite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                doc_type,
                number,
                title[:200] if title else number,
                title[:500] if title else '',
                'действует',
                '',
                '',
                content[:5000] if content else '',
                0
            ))
            added += 1
            
            if added % 50 == 0:
                print(f"Импортировано {added} документов...")
                
        except Exception as e:
            errors += 1
            print(f"Ошибка при импорте {filename}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"Импорт завершён!")
    print(f"✅ Успешно добавлено: {added}")
    print(f"❌ Ошибок: {errors}")
    print(f"📊 Всего в БД: {added}")
    print(f"{'='*50}")

if __name__ == '__main__':
    import_all_normatives()
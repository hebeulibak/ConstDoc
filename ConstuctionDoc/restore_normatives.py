import sqlite3
import json
import os

DB_PATH = "construction.db"

def restore_normatives():
    """Восстановление нормативов из JSON файла"""
    
    # Проверяем наличие JSON файла
    json_files = ['response.json', 'normatives.json', 'normatives_data.json']
    json_data = None
    
    for json_file in json_files:
        if os.path.exists(json_file):
            print(f"Найден файл: {json_file}")
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            break
    
    if not json_data:
        print("JSON файл с нормативами не найден!")
        print("Ищу альтернативные источники...")
        
        # Проверяем папку ConstuctionDoc
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.json') and ('norm' in file.lower() or 'normative' in file.lower()):
                    print(f"Найден возможный файл: {file}")
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            json_data = json.load(f)
                            print(f"Загружено из {file}")
                            break
                    except:
                        pass
            if json_data:
                break
    
    if not json_data:
        print("Не удалось найти файл с нормативами!")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Очищаем таблицу нормативов
    cursor.execute("DELETE FROM normatives")
    print("Таблица normatives очищена")
    
    # Восстанавливаем данные
    count = 0
    if isinstance(json_data, list):
        for item in json_data:
            try:
                cursor.execute('''
                    INSERT INTO normatives 
                    (doc_type, number, title, full_title, status, actual_date, tags, content, replaced_by, is_favorite)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item.get('doc_type', 'Документ'),
                    item.get('number', ''),
                    item.get('title', ''),
                    item.get('full_title', ''),
                    item.get('status', 'действует'),
                    item.get('actual_date', ''),
                    item.get('tags', ''),
                    item.get('content', ''),
                    item.get('replaced_by', None),
                    0
                ))
                count += 1
            except Exception as e:
                print(f"Ошибка при вставке: {e}")
    elif isinstance(json_data, dict):
        for key, item in json_data.items():
            try:
                cursor.execute('''
                    INSERT INTO normatives 
                    (doc_type, number, title, full_title, status, actual_date, tags, content, replaced_by, is_favorite)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item.get('doc_type', 'Документ'),
                    item.get('number', key),
                    item.get('title', ''),
                    item.get('full_title', ''),
                    item.get('status', 'действует'),
                    item.get('actual_date', ''),
                    item.get('tags', ''),
                    item.get('content', ''),
                    item.get('replaced_by', None),
                    0
                ))
                count += 1
            except Exception as e:
                print(f"Ошибка при вставке: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"Восстановлено {count} нормативных документов!")

if __name__ == '__main__':
    restore_normatives()
import sqlite3
import json
import os

DB_PATH = "construction.db"

def import_normatives_from_json(json_folder_path):
    """Импорт нормативов из JSON-файлов"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    
    # Проходим по всем JSON файлам в папке
    for filename in os.listdir(json_folder_path):
        if filename.endswith('.json'):
            filepath = os.path.join(json_folder_path, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    
                    # Проверяем структуру данных и извлекаем нужные поля
                    doc_number = data.get('number', '') or data.get('id', '') or filename.replace('.json', '')
                    doc_title = data.get('title', '') or data.get('full_name', '') or data.get('name', '')
                    
                    # Пропускаем, если нет названия
                    if not doc_title:
                        continue
                    
                    # Проверяем, существует ли уже такой документ
                    cursor.execute("SELECT id FROM normatives WHERE number = ?", (doc_number,))
                    existing = cursor.fetchone()
                    
                    if not existing:
                        cursor.execute('''INSERT INTO normatives 
                            (doc_type, number, title, full_title, status, actual_date, tags, content, is_favorite)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (
                                data.get('type', 'Документ')[:20],
                                doc_number[:50],
                                doc_title[:200],
                                data.get('full_name', '')[:500],
                                data.get('status', 'Неизвестно'),
                                data.get('actual_date', ''),
                                data.get('tags', ''),
                                data.get('content', '') or data.get('description', ''),
                                0
                            ))
                        count += 1
                        print(f"✅ Добавлен: {doc_number} - {doc_title[:50]}...")
                    else:
                        print(f"⏭️ Пропущен (уже есть): {doc_number}")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ Ошибка в файле {filename}: {e}")
                except Exception as e:
                    print(f"❌ Ошибка при обработке {filename}: {e}")
    
    conn.commit()
    conn.close()
    print(f"\n🎉 Импорт завершён! Добавлено {count} нормативов.")

if __name__ == "__main__":
    # Укажите путь к папке с JSON-файлами
    json_path = input("Введите путь к папке с JSON-файлами: ")
    
    if os.path.exists(json_path):
        import_normatives_from_json(json_path)
    else:
        print(f"Папка {json_path} не найдена!")
        print("Укажите правильный путь к папке, которую вы скачали с GitHub.")
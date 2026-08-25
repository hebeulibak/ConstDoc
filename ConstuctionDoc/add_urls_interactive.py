import sqlite3
import webbrowser
import time

DB_PATH = "construction.db"

def find_and_add_urls():
    """Интерактивный режим добавления ссылок"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Добавляем колонку url, если её нет
    try:
        cursor.execute("ALTER TABLE normatives ADD COLUMN url TEXT")
        print("✅ Добавлено поле url в таблицу")
    except sqlite3.OperationalError:
        print("⏩ Поле url уже существует")
    
    # Получаем документы без ссылок
    cursor.execute("SELECT id, number, title, full_title FROM normatives WHERE url IS NULL OR url = '' ORDER BY number")
    docs = cursor.fetchall()
    
    print("\n" + "=" * 60)
    print(f"📊 Найдено документов без ссылок: {len(docs)}")
    print("=" * 60)
    print("\n🔍 Сейчас вы сможете найти ссылки для каждого документа")
    print("   Будет открываться страница поиска в браузере")
    print("   Инструкция:")
    print("   1. В открывшемся окне найдите нужный документ")
    print("   2. Скопируйте ссылку из адресной строки")
    print("   3. Вставьте ссылку в консоль")
    print("   4. Нажмите Enter без ввода - пропустить документ")
    print("   q - завершить досрочно\n")
    
    input("Нажмите Enter, чтобы начать...")
    
    updated = 0
    skipped = 0
    
    for i, (doc_id, number, title, full_title) in enumerate(docs, 1):
        print("\n" + "=" * 60)
        print(f"[{i}/{len(docs)}] {number}")
        print("=" * 60)
        print(f"📄 Название: {full_title[:100] if full_title else title}")
        print()
        
        # Открываем поиск в браузере
        search_url = f"https://www.google.com/search?q={number}+site%3Adocs.cntd.ru"
        print(f"🔗 Открываю поиск: {search_url}")
        webbrowser.open(search_url)
        
        # Даём время на поиск
        print("\n⏳ Ищите документ в открывшемся окне браузера...")
        print("   Когда найдёте, скопируйте ссылку из адресной строки")
        print()
        
        url = input("📎 Вставьте ссылку (Enter - пропустить, q - выйти): ").strip()
        
        if url.lower() == 'q':
            print("\n⏹️ Досрочное завершение")
            break
        elif url and url.startswith('http'):
            cursor.execute("UPDATE normatives SET url = ? WHERE id = ?", (url, doc_id))
            updated += 1
            print(f"   ✅ Ссылка добавлена для {number}")
        else:
            skipped += 1
            print(f"   ⏭️ Документ {number} пропущен")
        
        # Небольшая пауза между документами
        if i < len(docs):
            print("\n⏳ Переход к следующему документу через 2 секунды...")
            time.sleep(2)
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТ:")
    print("=" * 60)
    print(f"   ✅ Добавлено ссылок: {updated}")
    print(f"   ⏭️ Пропущено: {skipped}")
    print(f"   📚 Всего обработано: {updated + skipped}")
    
    if updated > 0:
        print("\n🎉 Готово! Перезапустите приложение: python app.py")

def show_statistics():
    """Показывает статистику по ссылкам"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM normatives")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM normatives WHERE url IS NOT NULL AND url != ''")
    with_url = cursor.fetchone()[0]
    
    print("\n" + "=" * 60)
    print("📊 ТЕКУЩАЯ СТАТИСТИКА:")
    print("=" * 60)
    print(f"   📄 Всего документов: {total}")
    print(f"   🔗 Со ссылками: {with_url}")
    print(f"   ❌ Без ссылок: {total - with_url}")
    print(f"   📈 Процент: {with_url/total*100:.1f}%")
    
    conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🔗 ИНТЕРАКТИВНОЕ ДОБАВЛЕНИЕ ССЫЛОК НА ДОКУМЕНТЫ")
    print("=" * 60)
    
    show_statistics()
    
    print()
    choice = input("Начать добавление ссылок? (y/n): ").lower()
    
    if choice == 'y':
        find_and_add_urls()
    else:
        print("Операция отменена")
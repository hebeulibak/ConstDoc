# knowledge_base.py
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
from models import KnowledgeTip
from database import get_db_connection, DB_PATH

# Предустановленные подсказки для строителя
DEFAULT_TIPS = [
    {
        "category": "Фундаментные работы",
        "title": "Как правильно залить ленточный фундамент",
        "content": "Ленточный фундамент заливается при температуре не ниже +5°C. Бетон должен быть марки не ниже М300.",
        "steps": "1. Разметка участка\n2. Рытьё траншеи\n3. Установка опалубки\n4. Армирование\n5. Заливка бетона\n6. Уход за бетоном",
        "materials": "Цемент М400, песок, щебень, арматура d12, доска для опалубки",
        "safety": "Использовать перчатки, защитные очки. Не работать в одиночку."
    },
    {
        "category": "Кровельные работы",
        "title": "Монтаж металлочерепицы",
        "content": "Листы поднимаются на крышу по 2-3 штуки. Нахлёст должен быть не менее 10 см.",
        "steps": "1. Устройство стропильной системы\n2. Установка обрешётки\n3. Пароизоляция\n4. Укладка металлочерепицы\n5. Монтаж конька и торцевых планок",
        "materials": "Металлочерепица, саморезы с резиновой шайбой, гидроизоляция",
        "safety": "Работать со страховочным тросом. В обуви с мягкой подошвой."
    },
    {
        "category": "Электромонтажные работы",
        "title": "Установка розетки",
        "content": "Цветовая маркировка: коричневый/чёрный - фаза, синий - ноль, жёлто-зелёный - земля.",
        "steps": "1. Отключить электричество\n2. Зачистить провода\n3. Подключить к клеммам (фаза-ноль-земля)\n4. Закрепить в подрозетнике\n5. Установить крышку",
        "materials": "Розетка, индикаторная отвёртка, изолента",
        "safety": "ОБЯЗАТЕЛЬНО отключить автомат! Проверить отсутствие напряжения индикатором."
    },
    {
        "category": "Штукатурные работы",
        "title": "Штукатурка стен по маякам",
        "content": "Толщина слоя штукатурки не более 20-30 мм за один проход.",
        "steps": "1. Грунтовка стен\n2. Установка маячков\n3. Нанесение раствора\n4. Выравнивание правилом\n5. Затирка",
        "materials": "Штукатурная смесь, маячки 6 мм, правило, грунтовка",
        "safety": "Использовать перчатки, респиратор при замешивании."
    },
    {
        "category": "Сантехнические работы",
        "title": "Монтаж унитаза",
        "content": "Расстояние от стены до унитаза должно быть не менее 30 см.",
        "steps": "1. Установка гофры\n2. Разметка креплений\n3. Сверление отверстий\n4. Установка унитаза\n5. Подключение воды\n6. Герметизация стыка",
        "materials": "Унитаз, гофра, силиконовый герметик, дюбели",
        "safety": "Проверить отсутствие протечек после подключения."
    },
    {
        "category": "Бетонные работы",
        "title": "Правильное армирование фундамента",
        "content": "Защитный слой бетона должен быть 50-70 мм. Арматура не должна касаться опалубки.",
        "steps": "1. Подготовка арматуры\n2. Вязка сетки\n3. Установка фиксаторов\n4. Монтаж в опалубку\n5. Проверка защитного слоя",
        "materials": "Арматура d12-d16, вязальная проволока, крючок для вязки",
        "safety": "Работать в перчатках. Не ходить по арматуре."
    },
    {
        "category": "Земляные работы",
        "title": "Разработка котлована экскаватором",
        "content": "Глубина котлована не должна превышать проектную более чем на 10 см. Недобор грунта добирается вручную.",
        "steps": "1. Геодезическая разбивка\n2. Снятие растительного слоя\n3. Разработка грунта экскаватором\n4. Добор грунта вручную\n5. Планировка дна\n6. Устройство песчаной подушки",
        "materials": "Геодезические приборы, экскаватор, песок для подушки",
        "safety": "Запрещено находиться в зоне работы экскаватора. Установить ограждение котлована."
    },
    {
        "category": "Отделочные работы",
        "title": "Поклейка обоев",
        "content": "Температура в помещении должна быть не ниже +10°C. Окна и двери должны быть закрыты.",
        "steps": "1. Подготовка стен (шпаклёвка, грунтовка)\n2. Нарезка полотен\n3. Нанесение клея\n4. Поклейка\n5. Разглаживание\n6. Обрезка краёв",
        "materials": "Обои, клей для обоев, валик, шпатель, нож",
        "safety": "Избегать сквозняков до полного высыхания."
    }
]

def init_knowledge_base():
    """Инициализация базы знаний начальными данными"""
    try:
        # Проверяем существование таблицы и создаём при необходимости
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Проверяем, существует ли таблица knowledge_base
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge_base'")
            table_exists = cursor.fetchone()
            
            if not table_exists:
                # Создаём таблицу, если её нет
                cursor.execute('''CREATE TABLE IF NOT EXISTS knowledge_base
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     category TEXT,
                     title TEXT NOT NULL,
                     content TEXT,
                     steps TEXT,
                     materials TEXT,
                     safety TEXT,
                     image_path TEXT,
                     created_at TEXT)''')
                print("✅ Таблица knowledge_base создана")
        
        # Теперь заполняем данными
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Проверяем, пустая ли таблица
            cursor.execute("SELECT COUNT(*) FROM knowledge_base")
            count = cursor.fetchone()[0]
            
            if count == 0:
                for tip in DEFAULT_TIPS:
                    cursor.execute('''INSERT INTO knowledge_base 
                        (category, title, content, steps, materials, safety, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (tip['category'], tip['title'], tip['content'], 
                         tip['steps'], tip['materials'], tip['safety'],
                         datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                
                print(f"✅ База знаний инициализирована. Добавлено {len(DEFAULT_TIPS)} подсказок.")
            else:
                print(f"ℹ️ База знаний уже содержит данные. Найдено {count} подсказок.")
    
    except sqlite3.Error as e:
        print(f"❌ Ошибка базы данных при инициализации знаний: {e}")
        raise
    except Exception as e:
        print(f"❌ Ошибка при инициализации знаний: {e}")
        raise

def get_all_tips(category: Optional[str] = None, search: Optional[str] = None) -> List[KnowledgeTip]:
    """Получить все подсказки с фильтрацией"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM knowledge_base"
            params = []
            conditions = []
            
            if category and category != "Все" and category != "":
                conditions.append("category = ?")
                params.append(category)
            
            if search:
                conditions.append("(title LIKE ? OR content LIKE ? OR steps LIKE ?)")
                search_pattern = f"%{search}%"
                params.extend([search_pattern, search_pattern, search_pattern])
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY id"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Преобразуем строки в объекты KnowledgeTip
            tips = []
            for row in rows:
                tip_dict = dict(row)
                tip = KnowledgeTip(
                    id=tip_dict['id'],
                    category=tip_dict.get('category', ''),
                    title=tip_dict.get('title', ''),
                    content=tip_dict.get('content', ''),
                    steps=tip_dict.get('steps', ''),
                    materials=tip_dict.get('materials', ''),
                    safety=tip_dict.get('safety', ''),
                    image_path=tip_dict.get('image_path', ''),
                    created_at=tip_dict.get('created_at', '')
                )
                tips.append(tip)
            
            return tips
    except Exception as e:
        print(f"❌ Ошибка при получении подсказок: {e}")
        return []

def get_tip_by_id(tip_id: int) -> Optional[KnowledgeTip]:
    """Получить одну подсказку по ID"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM knowledge_base WHERE id = ?", (tip_id,))
            row = cursor.fetchone()
            
            if row:
                tip_dict = dict(row)
                return KnowledgeTip(
                    id=tip_dict['id'],
                    category=tip_dict.get('category', ''),
                    title=tip_dict.get('title', ''),
                    content=tip_dict.get('content', ''),
                    steps=tip_dict.get('steps', ''),
                    materials=tip_dict.get('materials', ''),
                    safety=tip_dict.get('safety', ''),
                    image_path=tip_dict.get('image_path', ''),
                    created_at=tip_dict.get('created_at', '')
                )
            return None
    except Exception as e:
        print(f"❌ Ошибка при получении подсказки {tip_id}: {e}")
        return None

def add_tip(category: str, title: str, content: str, steps: str = "", materials: str = "", safety: str = "") -> Optional[int]:
    """Добавить новую подсказку"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO knowledge_base 
                (category, title, content, steps, materials, safety, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (category, title, content, steps, materials, safety,
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            return cursor.lastrowid
    except Exception as e:
        print(f"❌ Ошибка при добавлении подсказки: {e}")
        return None

def update_tip(tip_id: int, category: str, title: str, content: str, 
               steps: str = "", materials: str = "", safety: str = "") -> bool:
    """Обновить существующую подсказку"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE knowledge_base 
                SET category=?, title=?, content=?, steps=?, materials=?, safety=?
                WHERE id=?''',
                (category, title, content, steps, materials, safety, tip_id))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"❌ Ошибка при обновлении подсказки {tip_id}: {e}")
        return False

def delete_tip(tip_id: int) -> bool:
    """Удалить подсказку"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM knowledge_base WHERE id = ?", (tip_id,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"❌ Ошибка при удалении подсказки {tip_id}: {e}")
        return False

def get_categories() -> List[str]:
    """Получить все категории"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM knowledge_base WHERE category != '' ORDER BY category")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
    except Exception as e:
        print(f"❌ Ошибка при получении категорий: {e}")
        return []

def get_tips_by_category(category: str) -> List[KnowledgeTip]:
    """Получить подсказки по категории"""
    return get_all_tips(category=category)

def search_tips(query: str) -> List[KnowledgeTip]:
    """Поиск подсказок по тексту"""
    return get_all_tips(search=query)

def get_tip_count() -> int:
    """Получить общее количество подсказок"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM knowledge_base")
            return cursor.fetchone()[0]
    except Exception as e:
        print(f"❌ Ошибка при подсчёте подсказок: {e}")
        return 0

def get_category_stats() -> Dict[str, int]:
    """Получить статистику по категориям"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT category, COUNT(*) as count 
                FROM knowledge_base 
                GROUP BY category 
                ORDER BY count DESC
            """)
            rows = cursor.fetchall()
            return {row[0]: row[1] for row in rows if row[0]}
    except Exception as e:
        print(f"❌ Ошибка при получении статистики категорий: {e}")
        return {}

if __name__ == "__main__":
    # Для тестирования
    init_knowledge_base()
    print(f"Всего подсказок: {get_tip_count()}")
    print(f"Категории: {get_categories()}")
    print(f"Статистика: {get_category_stats()}")
    
    # Пример поиска
    results = search_tips("фундамент")
    print(f"Найдено по запросу 'фундамент': {len(results)}")
import sqlite3
import os
from contextlib import contextmanager
from models import ConstructionSite, GeneralJournalEntry, NormativeDocument, NormDocType, PhotoWithLocation, Document

DB_PATH = "construction.db"

# Контекстный менеджер для работы с БД
@contextmanager
def get_db_connection():
    """Контекстный менеджер для автоматического открытия/закрытия соединения"""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        # Устанавливаем UTF-8 кодировку
        conn.execute("PRAGMA encoding = 'UTF-8'")
        # Включаем поддержку FOREIGN KEY
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        print(f"Ошибка базы данных: {e}")
        raise
    finally:
        if conn:
            conn.close()

def init_db():
    """Инициализация базы данных со всеми таблицами и внешними ключами"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Включаем поддержку внешних ключей
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Таблица объектов
        cursor.execute('''CREATE TABLE IF NOT EXISTS sites
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      name TEXT NOT NULL, address TEXT, customer TEXT, contractor TEXT, 
                      start_date TEXT, end_date TEXT)''')
        
        # Таблица журнала работ (с FOREIGN KEY)
        cursor.execute('''CREATE TABLE IF NOT EXISTS general_journal
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      site_id INTEGER, date TEXT NOT NULL, work_type TEXT, work_description TEXT,
                      location TEXT, executor TEXT, responsible_person TEXT, workers_count INTEGER, 
                      shift TEXT, start_time TEXT, end_time TEXT, volume REAL, volume_unit TEXT, 
                      equipment_used TEXT, materials_used TEXT, notes TEXT, weather TEXT, 
                      temperature REAL, created_at TEXT, updated_at TEXT,
                      FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE)''')
        
        # Таблица нормативов
        cursor.execute('''CREATE TABLE IF NOT EXISTS normatives
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      doc_type TEXT, number TEXT, title TEXT, full_title TEXT,
                      status TEXT, actual_date TEXT, tags TEXT, content TEXT, 
                      replaced_by TEXT, is_favorite INTEGER DEFAULT 0)''')
        
        # Создаём индекс для полнотекстового поиска по нормативам
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_normatives_search 
                          ON normatives(number, title, tags)''')
        
        # Таблица фото (с FOREIGN KEY)
        cursor.execute('''CREATE TABLE IF NOT EXISTS photos
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      site_id INTEGER, photo_path TEXT NOT NULL, 
                      latitude REAL, longitude REAL, timestamp TEXT, 
                      description TEXT, document_section TEXT,
                      FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE)''')
        
        # Таблица документов (с FOREIGN KEY)
        cursor.execute('''CREATE TABLE IF NOT EXISTS documents
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      site_id INTEGER, section TEXT, title TEXT NOT NULL, 
                      document_number TEXT, date TEXT, description TEXT, 
                      file_path TEXT, created_at TEXT,
                      FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE)''')
        
        # Таблица базы знаний (подсказки)
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
        
        # Таблица для связи журнала и фото (многие-ко-многим)
        cursor.execute('''CREATE TABLE IF NOT EXISTS journal_photos
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      journal_entry_id INTEGER,
                      photo_path TEXT,
                      FOREIGN KEY (journal_entry_id) REFERENCES general_journal(id) ON DELETE CASCADE)''')
        
        conn.commit()

# ============ ОБЪЕКТЫ ============
def get_all_sites():
    """Получить все строительные объекты"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sites ORDER BY id DESC")
        rows = cursor.fetchall()
        return [ConstructionSite(**dict(row)) for row in rows]

def get_site_by_id(site_id):
    """Получить объект по ID"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sites WHERE id = ?", (site_id,))
            row = cursor.fetchone()
            if row:
                return ConstructionSite(**dict(row))
            return None
    except sqlite3.Error as e:
        print(f"Ошибка при получении объекта {site_id}: {e}")
        return None

def add_site(site):
    """Добавить новый объект"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO sites (name, address, customer, contractor, start_date, end_date)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (site.name, site.address, site.customer, site.contractor, 
                            site.start_date, site.end_date))
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении объекта: {e}")
        return None

def update_site(site):
    """Обновить данные объекта"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE sites 
                              SET name=?, address=?, customer=?, contractor=?, 
                                  start_date=?, end_date=?
                              WHERE id=?''',
                           (site.name, site.address, site.customer, site.contractor, 
                            site.start_date, site.end_date, site.id))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении объекта {site.id}: {e}")
        return False

def delete_site(site_id):
    """Удалить объект и все связанные данные (каскадно)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Благодаря FOREIGN KEY ON DELETE CASCADE, связанные записи удалятся автоматически
            cursor.execute("DELETE FROM sites WHERE id = ?", (site_id,))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Ошибка при удалении объекта {site_id}: {e}")
        return False

# ============ ЖУРНАЛ РАБОТ ============
def get_journal_entries(site_id, limit=None):
    """Получить записи журнала для объекта"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM general_journal WHERE site_id = ? ORDER BY date DESC, id DESC"
        if limit:
            query += " LIMIT ?"
            cursor.execute(query, (site_id, limit))
        else:
            cursor.execute(query, (site_id,))
        
        rows = cursor.fetchall()
        entries = []
        for row in rows:
            entry_dict = dict(row)
            # Получаем фото для этой записи
            cursor.execute("SELECT photo_path FROM journal_photos WHERE journal_entry_id = ?", (entry_dict['id'],))
            photos = [p['photo_path'] for p in cursor.fetchall()]
            entry_dict['photo_paths'] = ','.join(photos) if photos else ''
            entries.append(GeneralJournalEntry(**entry_dict))
        return entries

def add_journal_entry(entry):
    """Добавить запись в журнал"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO general_journal 
                (site_id, date, work_type, work_description, location, executor, responsible_person, 
                 workers_count, shift, start_time, end_time, volume, volume_unit, equipment_used, 
                 materials_used, notes, weather, temperature, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (entry.site_id, entry.date, entry.work_type, entry.work_description, 
                 entry.location, entry.executor, entry.responsible_person, entry.workers_count, 
                 entry.shift, entry.start_time, entry.end_time, entry.volume, entry.volume_unit, 
                 entry.equipment_used, entry.materials_used, entry.notes, entry.weather, 
                 entry.temperature, entry.created_at, entry.updated_at))
            
            entry_id = cursor.lastrowid
            
            # Сохраняем фото в отдельную таблицу
            if entry.photo_paths:
                photos = entry.photo_paths.split(',')
                for photo_path in photos:
                    if photo_path.strip():
                        cursor.execute("INSERT INTO journal_photos (journal_entry_id, photo_path) VALUES (?, ?)",
                                     (entry_id, photo_path.strip()))
            
            return entry_id
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении записи журнала: {e}")
        return None

def get_journal_entry_by_id(entry_id):
    """Получить запись журнала по ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM general_journal WHERE id = ?", (entry_id,))
        row = cursor.fetchone()
        if row:
            entry_dict = dict(row)
            # Получаем фото для этой записи
            cursor.execute("SELECT photo_path FROM journal_photos WHERE journal_entry_id = ?", (entry_id,))
            photos = [p['photo_path'] for p in cursor.fetchall()]
            entry_dict['photo_paths'] = ','.join(photos) if photos else ''
            return GeneralJournalEntry(**entry_dict)
        return None

def update_journal_entry(entry):
    """Обновить запись журнала"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE general_journal SET 
                date=?, work_type=?, work_description=?, location=?, executor=?, 
                responsible_person=?, workers_count=?, shift=?, start_time=?, end_time=?,
                volume=?, volume_unit=?, equipment_used=?, materials_used=?, notes=?, 
                weather=?, temperature=?, updated_at=?
                WHERE id=?''',
                (entry.date, entry.work_type, entry.work_description, entry.location, 
                 entry.executor, entry.responsible_person, entry.workers_count, entry.shift, 
                 entry.start_time, entry.end_time, entry.volume, entry.volume_unit, 
                 entry.equipment_used, entry.materials_used, entry.notes, entry.weather, 
                 entry.temperature, entry.updated_at, entry.id))
            
            # Обновляем фото: удаляем старые и добавляем новые
            cursor.execute("DELETE FROM journal_photos WHERE journal_entry_id = ?", (entry.id,))
            if entry.photo_paths:
                photos = entry.photo_paths.split(',')
                for photo_path in photos:
                    if photo_path.strip():
                        cursor.execute("INSERT INTO journal_photos (journal_entry_id, photo_path) VALUES (?, ?)",
                                     (entry.id, photo_path.strip()))
            
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении записи журнала {entry.id}: {e}")
        return False

def delete_journal_entry(entry_id):
    """Удалить запись журнала"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM general_journal WHERE id = ?", (entry_id,))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Ошибка при удалении записи журнала {entry_id}: {e}")
        return False

def get_journal_summary(site_id):
    """Получить статистику по журналу"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM general_journal WHERE site_id = ?", (site_id,))
        total = cursor.fetchone()[0]
        cursor.execute('''SELECT date, COUNT(*) as count FROM general_journal 
                          WHERE site_id = ? AND date >= date('now', '-7 days') 
                          GROUP BY date ORDER BY date''', (site_id,))
        weekly = cursor.fetchall()
        return {"total_entries": total, "weekly_stats": [(row['date'], row['count']) for row in weekly]}

# ============ ФОТО ============
def add_photo(photo):
    """Добавить фото"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO photos (site_id, photo_path, latitude, longitude, timestamp, description, document_section)
                              VALUES (?,?,?,?,?,?,?)''',
                           (photo.site_id, photo.photo_path, photo.latitude, photo.longitude, 
                            photo.timestamp, photo.description, photo.document_section))
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении фото: {e}")
        return None

def get_photos_by_site(site_id, section=None):
    """Получить фото для объекта"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if section:
            cursor.execute("SELECT * FROM photos WHERE site_id = ? AND document_section = ? ORDER BY timestamp DESC", 
                           (site_id, section))
        else:
            cursor.execute("SELECT * FROM photos WHERE site_id = ? ORDER BY timestamp DESC", (site_id,))
        rows = cursor.fetchall()
        return [PhotoWithLocation(**dict(row)) for row in rows]

def delete_photo(photo_id):
    """Удалить фото"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Сначала получаем путь к файлу
            cursor.execute("SELECT photo_path FROM photos WHERE id = ?", (photo_id,))
            row = cursor.fetchone()
            if row and row['photo_path']:
                # Удаляем физический файл
                try:
                    if os.path.exists(row['photo_path']):
                        os.remove(row['photo_path'])
                except Exception as e:
                    print(f"Ошибка удаления файла: {e}")
            
            cursor.execute("DELETE FROM photos WHERE id = ?", (photo_id,))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Ошибка при удалении фото {photo_id}: {e}")
        return False

# ============ ДОКУМЕНТЫ ============
def add_document(doc):
    """Добавить документ"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO documents (site_id, section, title, document_number, date, description, file_path, created_at)
                              VALUES (?,?,?,?,?,?,?,?)''',
                           (doc.site_id, doc.section, doc.title, doc.document_number, 
                            doc.date, doc.description, doc.file_path, doc.created_at))
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении документа: {e}")
        return None

def get_documents_by_site(site_id, section=None):
    """Получить документы для объекта"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if section:
            cursor.execute("SELECT * FROM documents WHERE site_id = ? AND section = ? ORDER BY date DESC", 
                           (site_id, section))
        else:
            cursor.execute("SELECT * FROM documents WHERE site_id = ? ORDER BY date DESC", (site_id,))
        rows = cursor.fetchall()
        return [Document(**dict(row)) for row in rows]

def delete_document(doc_id):
    """Удалить документ"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Ошибка при удалении документа {doc_id}: {e}")
        return False

def get_document_by_id(doc_id):
    """Получить документ по ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        if row:
            return Document(**dict(row))
        return None

# ============ НОРМАТИВЫ ============
def get_all_normatives(doc_type=None, search=""):
    """Получить все нормативные документы с фильтрацией"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM normatives"
        params = []
        conditions = []
        
        if doc_type and doc_type != "Все" and doc_type != "":
            conditions.append("doc_type = ?")
            params.append(doc_type)
        
        if search:
            conditions.append("(number LIKE ? OR title LIKE ? OR tags LIKE ? OR content LIKE ?)")
            search_pattern = f"%{search}%"
            params.extend([search_pattern, search_pattern, search_pattern, search_pattern])
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY is_favorite DESC, number"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            row_dict = dict(row)
            # Преобразуем doc_type в Enum, если нужно
            if 'doc_type' in row_dict and row_dict['doc_type']:
                try:
                    row_dict['doc_type'] = NormDocType(row_dict['doc_type'])
                except ValueError:
                    # Если значение не соответствует Enum, оставляем как строку
                    pass
            row_dict['is_favorite'] = bool(row_dict.get('is_favorite', 0))
            result.append(NormativeDocument(**row_dict))
        return result

def get_normative_by_id(doc_id):
    """Получить нормативный документ по ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM normatives WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        if row:
            row_dict = dict(row)
            if 'doc_type' in row_dict and row_dict['doc_type']:
                try:
                    row_dict['doc_type'] = NormDocType(row_dict['doc_type'])
                except ValueError:
                    pass
            row_dict['is_favorite'] = bool(row_dict.get('is_favorite', 0))
            return NormativeDocument(**row_dict)
        return None

def toggle_favorite(doc_id, is_favorite):
    """Переключить статус избранного"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE normatives SET is_favorite = ? WHERE id = ?", 
                           (1 if is_favorite else 0, doc_id))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении статуса избранного для {doc_id}: {e}")
        return False

def add_normative(normative):
    """Добавить новый нормативный документ"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            doc_type_value = normative.doc_type.value if hasattr(normative.doc_type, 'value') else str(normative.doc_type)
            cursor.execute('''INSERT INTO normatives 
                              (doc_type, number, title, full_title, status, actual_date, 
                               tags, content, replaced_by, is_favorite)
                              VALUES (?,?,?,?,?,?,?,?,?,?)''',
                           (doc_type_value, normative.number, normative.title, 
                            normative.full_title, normative.status, normative.actual_date,
                            normative.tags, normative.content, normative.replaced_by,
                            1 if normative.is_favorite else 0))
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении норматива: {e}")
        return None

# ============ ПОИСК И ФИЛЬТРАЦИЯ В ЖУРНАЛЕ ============

def get_journal_entries_filtered(site_id, search='', date_from='', date_to='', work_type='', responsible=''):
    """Получить записи журнала с фильтрацией"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM general_journal WHERE site_id = ?"
        params = [site_id]
        
        if search:
            query += " AND (work_description LIKE ? OR work_type LIKE ? OR location LIKE ? OR notes LIKE ?)"
            search_pattern = f"%{search}%"
            params.extend([search_pattern, search_pattern, search_pattern, search_pattern])
        
        if date_from:
            query += " AND date >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND date <= ?"
            params.append(date_to)
        
        if work_type:
            query += " AND work_type = ?"
            params.append(work_type)
        
        if responsible:
            query += " AND responsible_person = ?"
            params.append(responsible)
        
        query += " ORDER BY date DESC, id DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        entries = []
        for row in rows:
            entry_dict = dict(row)
            cursor.execute("SELECT photo_path FROM journal_photos WHERE journal_entry_id = ?", (entry_dict['id'],))
            photos = [p['photo_path'] for p in cursor.fetchall()]
            entry_dict['photo_paths'] = ','.join(photos) if photos else ''
            entries.append(GeneralJournalEntry(**entry_dict))
        return entries

def get_distinct_work_types(site_id):
    """Получить уникальные типы работ для объекта"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT work_type FROM general_journal WHERE site_id = ? AND work_type != '' ORDER BY work_type", (site_id,))
        rows = cursor.fetchall()
        return [row[0] for row in rows]

def get_distinct_responsible(site_id):
    """Получить уникальных ответственных для объекта"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT responsible_person FROM general_journal WHERE site_id = ? AND responsible_person != '' ORDER BY responsible_person", (site_id,))
        rows = cursor.fetchall()
        return [row[0] for row in rows]

def get_journal_entries_by_date_range(site_id, start_date, end_date):
    """Получить записи журнала за период"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM general_journal 
                         WHERE site_id = ? AND date BETWEEN ? AND ? 
                         ORDER BY date""", (site_id, start_date, end_date))
        rows = cursor.fetchall()
        return [GeneralJournalEntry(**dict(row)) for row in rows]

def get_work_types_stats(site_id):
    """Получить статистику по типам работ"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT work_type, COUNT(*) as count, SUM(volume) as total_volume
                         FROM general_journal 
                         WHERE site_id = ? AND work_type != ''
                         GROUP BY work_type
                         ORDER BY count DESC""", (site_id,))
        rows = cursor.fetchall()
        return [{"work_type": row[0], "count": row[1], "total_volume": row[2]} for row in rows]
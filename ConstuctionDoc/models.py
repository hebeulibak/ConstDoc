from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional, List, Any

# ============ ENUM ДЛЯ НОРМАТИВОВ ============
class NormDocType(Enum):
    SP = "СП"
    GOST = "ГОСТ"
    LAW = "Закон"
    DECREE = "Приказ"
    DOCUMENT = "Документ"
    SNIP = "СНиП"  # Убираем дублирование, оставляем один
    SANPIN = "СанПиН"
    STANDARD = "Стандарт"
    CODE = "Свод правил"
    RULE = "Правила"
    ORDER = "Приказ"
    MANUAL = "Пособие"
    OTHER = "Прочие"

class DocumentSection(Enum):
    INCOMING = "Входящие документы"
    OUTGOING = "Исходящие документы"
    ACTS = "Акты"
    JOURNALS = "Журналы"
    EXECUTIVE = "Исполнительная документация"

# ============ МОДЕЛЬ ПОЛЬЗОВАТЕЛЯ ============
@dataclass
class User:
    """Модель пользователя для аутентификации"""
    id: int
    username: str
    password_hash: str
    is_admin: bool = False
    full_name: str = ""
    email: str = ""
    created_at: str = ""
    last_login: str = ""

# ============ МОДЕЛЬ ОБЪЕКТА СТРОИТЕЛЬСТВА ============
@dataclass
class ConstructionSite:
    id: int
    name: str
    address: str
    customer: str
    contractor: str
    start_date: str
    end_date: str = None

# ============ МОДЕЛЬ ЗАПИСИ ЖУРНАЛА РАБОТ ============
@dataclass
class GeneralJournalEntry:
    id: int
    site_id: int
    date: str
    work_type: str
    work_description: str
    location: str
    executor: str
    responsible_person: str
    workers_count: int
    shift: str
    start_time: str
    end_time: str
    volume: float
    volume_unit: str
    equipment_used: str
    materials_used: str
    notes: str
    weather: str
    temperature: float
    photo_paths: str
    created_at: str
    updated_at: str

# ============ МОДЕЛЬ ФОТО С ГЕОЛОКАЦИЕЙ ============
@dataclass
class PhotoWithLocation:
    id: int
    site_id: int
    photo_path: str
    latitude: float
    longitude: float
    timestamp: str
    description: str
    document_section: str

# ============ МОДЕЛЬ ДОКУМЕНТА ============
@dataclass
class Document:
    id: int
    site_id: int
    section: str
    title: str
    document_number: str
    date: str
    description: str
    file_path: str
    created_at: str

# ============ МОДЕЛЬ НОРМАТИВНОГО ДОКУМЕНТА ============
@dataclass
class NormativeDocument:
    id: int
    doc_type: NormDocType
    number: str
    title: str
    full_title: str
    status: str
    actual_date: str
    tags: str
    content: str
    replaced_by: str = None
    is_favorite: bool = False
    url: str = None  # Для совместимости, хотя в БД нет этого поля

# ============ МОДЕЛЬ ДЛЯ БАЗЫ ЗНАНИЙ ============
@dataclass
class KnowledgeTip:
    """Модель подсказки из базы знаний"""
    id: int
    category: str
    title: str
    content: str
    steps: str = ""
    materials: str = ""
    safety: str = ""
    image_path: str = ""
    created_at: str = ""

# ============ ПОЛНЫЙ ПЕРЕЧЕНЬ ВИДОВ РАБОТ (136 видов) ============
class WorkType(Enum):
    # 1. Подготовительные работы
    CLEARING_SITE = "Расчистка площадки"
    DEMOLITION = "Демонтаж зданий"
    GEODESY = "Геодезические работы"
    SITE_PLANNING = "Вертикальная планировка"
    UTILITIES_RELOCATION = "Перекладка коммуникаций"
    
    # 2. Земляные работы
    EARTH_EXCAVATION = "Разработка грунта экскаватором"
    EARTH_MANUAL = "Разработка грунта вручную"
    EARTH_BACKFILL = "Обратная засыпка"
    EARTH_COMPACTION = "Уплотнение грунта"
    EARTH_TRENCH = "Рытье траншей"
    EARTH_PIT = "Разработка котлована"
    EARTH_IMPORT = "Подвоз грунта"
    EARTH_EXPORT = "Вывоз грунта"
    
    # 3. Свайные работы
    PILE_DRIVING = "Забивка свай"
    PILE_BORED = "Буронабивные сваи"
    PILE_SCREW = "Винтовые сваи"
    PILE_GROUTING = "Цементация свай"
    
    # 4. Фундаментные работы
    FOUNDATION_BLOCK = "Монтаж фундаментных блоков"
    FOUNDATION_MONOLITHIC = "Устройство монолитного фундамента"
    FOUNDATION_STRIP = "Ленточный фундамент"
    FOUNDATION_SLAB = "Плитный фундамент"
    FOUNDATION_COLUMN = "Столбчатый фундамент"
    FOUNDATION_WATERPROOFING = "Гидроизоляция фундамента"
    FOUNDATION_INSULATION = "Утепление фундамента"
    
    # 5. Бетонные работы
    CONCRETE_PREPARATION = "Бетонная подготовка"
    CONCRETE_FORMWORK = "Установка опалубки"
    CONCRETE_REINFORCEMENT = "Армирование"
    CONCRETE_POURING = "Укладка бетонной смеси"
    CONCRETE_VIBRATION = "Виброуплотнение бетона"
    CONCRETE_CURING = "Уход за бетоном"
    CONCRETE_STRIPPING = "Распалубка"
    CONCRETE_GROUTING = "Торкретирование"
    
    # 6. Каменные работы
    MASONRY_BRICK = "Кирпичная кладка"
    MASONRY_BLOCK = "Кладка из блоков"
    MASONRY_SILICATE = "Силикатная кладка"
    MASONRY_PARTITION = "Устройство перегородок"
    MASONRY_REINFORCED = "Армированная кладка"
    MASONRY_FACING = "Облицовочная кладка"
    
    # 7. Монтажные работы
    INSTALLATION_COLUMN = "Монтаж колонн"
    INSTALLATION_BEAM = "Монтаж балок"
    INSTALLATION_SLAB = "Монтаж плит перекрытия"
    INSTALLATION_TRUSS = "Монтаж ферм"
    INSTALLATION_METAL = "Монтаж металлоконструкций"
    INSTALLATION_CRANE = "Монтаж кранов"
    INSTALLATION_LIFT = "Монтаж лифтов"
    INSTALLATION_STAIRS = "Монтаж лестничных маршей"
    INSTALLATION_WINDOWS = "Монтаж оконных блоков"
    INSTALLATION_DOORS = "Монтаж дверных блоков"
    INSTALLATION_VENTILATION = "Монтаж вентблоков"
    
    # 8. Кровельные работы
    ROOF_RAFTER = "Устройство стропильной системы"
    ROOF_SHEATHING = "Устройство обрешетки"
    ROOF_COUNTER = "Устройство контробрешетки"
    ROOF_VAPOR_BARRIER = "Пароизоляция"
    ROOF_INSULATION = "Утепление кровли"
    ROOF_UNDERLAYMENT = "Подкровельная гидроизоляция"
    ROOF_METAL = "Монтаж металлочерепицы"
    ROOF_SOFT = "Монтаж мягкой кровли"
    ROOF_FLAT = "Устройство плоской кровли"
    ROOF_SEAM = "Фальцевая кровля"
    ROOF_COMPOSITE = "Композитная черепица"
    ROOF_DRAINAGE = "Монтаж водостоков"
    ROOF_SNOW_RETENTION = "Монтаж снегозадержателей"
    
    # 9. Отделочные работы
    FINISHING_PLASTER = "Штукатурные работы"
    FINISHING_PUTTY = "Шпатлевание"
    FINISHING_PAINT = "Окраска"
    FINISHING_WALLPAPER = "Оклейка обоями"
    FINISHING_TILE = "Облицовка плиткой"
    FINISHING_FLOOR_SCREED = "Устройство стяжки"
    FINISHING_FLOOR = "Устройство полов"
    FINISHING_CEILING = "Монтаж потолков"
    FINISHING_SUSPENDED = "Подвесные потолки"
    FINISHING_STRETCH = "Натяжные потолки"
    FINISHING_DECORATIVE = "Декоративная штукатурка"
    FINISHING_PANEL = "Монтаж стеновых панелей"
    
    # 10. Фасадные работы
    FACADE_INSULATION = "Утепление фасада"
    FACADE_PLASTER = "Фасадная штукатурка"
    FACADE_BRICK = "Облицовочный кирпич"
    FACADE_VENTILATED = "Вентилируемый фасад"
    FACADE_PANEL = "Фасадные панели"
    FACADE_PAINT = "Фасадная окраска"
    FACADE_CLADDING = "Клиновой фасад"
    
    # 11. Сантехнические работы
    PLUMBING_WATER = "Монтаж водоснабжения"
    PLUMBING_SEWER = "Монтаж канализации"
    PLUMBING_HEATING = "Монтаж отопления"
    PLUMBING_RADIATOR = "Установка радиаторов"
    PLUMBING_FLOOR_HEATING = "Теплый пол водяной"
    PLUMBING_BOILER = "Установка котла"
    PLUMBING_EQUIPMENT = "Установка сантехники"
    PLUMBING_PUMP = "Монтаж насосного оборудования"
    
    # 12. Электромонтажные работы
    ELECTRIC_CABLE = "Прокладка кабеля"
    ELECTRIC_PANEL = "Монтаж щитового оборудования"
    ELECTRIC_LIGHTING = "Монтаж освещения"
    ELECTRIC_GROUNDING = "Заземление"
    ELECTRIC_AUTOMATION = "Монтаж автоматики"
    ELECTRIC_SOCKET = "Установка розеток и выключателей"
    ELECTRIC_WARM_FLOOR = "Теплый пол электрический"
    
    # 13. Слаботочные системы
    LOW_CURRENT_NETWORK = "Монтаж слаботочных сетей"
    LOW_CURRENT_SECURITY = "Монтаж охранной сигнализации"
    LOW_CURRENT_VIDEO = "Монтаж видеонаблюдения"
    LOW_CURRENT_INTERNET = "Монтаж интернета и телефонии"
    LOW_CURRENT_FIRE = "Пожарная сигнализация"
    LOW_CURRENT_CONTROL = "Система контроля доступа"
    
    # 14. Вентиляция и кондиционирование
    HVAC_DUCT = "Монтаж воздуховодов"
    HVAC_EQUIPMENT = "Монтаж оборудования"
    HVAC_INSULATION = "Изоляция воздуховодов"
    HVAC_GRILLE = "Монтаж решеток и диффузоров"
    HVAC_SPLIT = "Монтаж сплит-систем"
    HVAC_VRV = "Монтаж VRV систем"
    
    # 15. Благоустройство
    LANDSCAPE_PAVING = "Мощение дорожек"
    LANDSCAPE_GREENING = "Озеленение"
    LANDSCAPE_FENCE = "Монтаж ограждений"
    LANDSCAPE_GATES = "Установка ворот"
    LANDSCAPE_LIGHTING = "Наружное освещение"
    LANDSCAPE_IRRIGATION = "Автополив"
    LANDSCAPE_PLAYGROUND = "Монтаж детской площадки"
    
    # 16. Пусконаладочные работы
    COMMISSIONING_ELECTRIC = "Пусконаладка электрооборудования"
    COMMISSIONING_PLUMBING = "Пусконаладка сантехники"
    COMMISSIONING_HVAC = "Пусконаладка вентиляции"
    COMMISSIONING_AUTOMATION = "Пусконаладка автоматики"
    
    # 17. Изоляционные работы
    INSULATION_THERMAL = "Теплоизоляция"
    INSULATION_WATER = "Гидроизоляция"
    INSULATION_SOUND = "Звукоизоляция"
    INSULATION_FIRE = "Огнезащита"
    
    # 18. Дорожные работы
    ROAD_BASE = "Устройство основания"
    ROAD_ASPHALT = "Асфальтирование"
    ROAD_CONCRETE = "Бетонирование"
    ROAD_CURB = "Установка бордюров"
    ROAD_MARKING = "Разметка"
    
    # 19. Монолитные работы
    MONOLITHIC_WALL = "Монолитные стены"
    MONOLITHIC_CEILING = "Монолитное перекрытие"
    MONOLITHIC_STAIRS = "Монолитная лестница"
    
    # 20. Прочие работы
    SCAFFOLDING = "Монтаж лесов"
    CRANE_OPERATION = "Работа крана"
    WASTE_REMOVAL = "Вывоз мусора"
    SNOW_CLEARING = "Очистка от снега"
    WATER_PUMPING = "Откачка воды"

    # Дополнительные методы для удобной работы с Enum
    @classmethod
    def get_all_values(cls):
        """Получить список всех значений"""
        return [work.value for work in cls]

    @classmethod
    def get_by_value(cls, value):
        """Получить элемент по значению"""
        for work in cls:
            if work.value == value:
                return work
        return None

    @classmethod
    def get_category_name(cls, work_type):
        """Получить категорию вида работ"""
        categories = {
            "Подготовительные": ["CLEARING_SITE", "DEMOLITION", "GEODESY", "SITE_PLANNING", "UTILITIES_RELOCATION"],
            "Земляные": ["EARTH_EXCAVATION", "EARTH_MANUAL", "EARTH_BACKFILL", "EARTH_COMPACTION", 
                        "EARTH_TRENCH", "EARTH_PIT", "EARTH_IMPORT", "EARTH_EXPORT"],
            "Свайные": ["PILE_DRIVING", "PILE_BORED", "PILE_SCREW", "PILE_GROUTING"],
            "Фундаментные": ["FOUNDATION_BLOCK", "FOUNDATION_MONOLITHIC", "FOUNDATION_STRIP", 
                           "FOUNDATION_SLAB", "FOUNDATION_COLUMN", "FOUNDATION_WATERPROOFING", "FOUNDATION_INSULATION"],
            "Бетонные": ["CONCRETE_PREPARATION", "CONCRETE_FORMWORK", "CONCRETE_REINFORCEMENT", 
                        "CONCRETE_POURING", "CONCRETE_VIBRATION", "CONCRETE_CURING", "CONCRETE_STRIPPING", "CONCRETE_GROUTING"],
            "Каменные": ["MASONRY_BRICK", "MASONRY_BLOCK", "MASONRY_SILICATE", "MASONRY_PARTITION", 
                        "MASONRY_REINFORCED", "MASONRY_FACING"],
            "Монтажные": ["INSTALLATION_COLUMN", "INSTALLATION_BEAM", "INSTALLATION_SLAB", "INSTALLATION_TRUSS",
                         "INSTALLATION_METAL", "INSTALLATION_CRANE", "INSTALLATION_LIFT", "INSTALLATION_STAIRS",
                         "INSTALLATION_WINDOWS", "INSTALLATION_DOORS", "INSTALLATION_VENTILATION"],
            "Кровельные": ["ROOF_RAFTER", "ROOF_SHEATHING", "ROOF_COUNTER", "ROOF_VAPOR_BARRIER", "ROOF_INSULATION",
                          "ROOF_UNDERLAYMENT", "ROOF_METAL", "ROOF_SOFT", "ROOF_FLAT", "ROOF_SEAM", "ROOF_COMPOSITE",
                          "ROOF_DRAINAGE", "ROOF_SNOW_RETENTION"],
            "Отделочные": ["FINISHING_PLASTER", "FINISHING_PUTTY", "FINISHING_PAINT", "FINISHING_WALLPAPER",
                          "FINISHING_TILE", "FINISHING_FLOOR_SCREED", "FINISHING_FLOOR", "FINISHING_CEILING",
                          "FINISHING_SUSPENDED", "FINISHING_STRETCH", "FINISHING_DECORATIVE", "FINISHING_PANEL"],
            "Фасадные": ["FACADE_INSULATION", "FACADE_PLASTER", "FACADE_BRICK", "FACADE_VENTILATED", 
                        "FACADE_PANEL", "FACADE_PAINT", "FACADE_CLADDING"],
            "Сантехнические": ["PLUMBING_WATER", "PLUMBING_SEWER", "PLUMBING_HEATING", "PLUMBING_RADIATOR",
                              "PLUMBING_FLOOR_HEATING", "PLUMBING_BOILER", "PLUMBING_EQUIPMENT", "PLUMBING_PUMP"],
            "Электромонтажные": ["ELECTRIC_CABLE", "ELECTRIC_PANEL", "ELECTRIC_LIGHTING", "ELECTRIC_GROUNDING",
                                "ELECTRIC_AUTOMATION", "ELECTRIC_SOCKET", "ELECTRIC_WARM_FLOOR"],
            "Слаботочные": ["LOW_CURRENT_NETWORK", "LOW_CURRENT_SECURITY", "LOW_CURRENT_VIDEO", "LOW_CURRENT_INTERNET",
                           "LOW_CURRENT_FIRE", "LOW_CURRENT_CONTROL"],
            "Вентиляция": ["HVAC_DUCT", "HVAC_EQUIPMENT", "HVAC_INSULATION", "HVAC_GRILLE", "HVAC_SPLIT", "HVAC_VRV"],
            "Благоустройство": ["LANDSCAPE_PAVING", "LANDSCAPE_GREENING", "LANDSCAPE_FENCE", "LANDSCAPE_GATES",
                               "LANDSCAPE_LIGHTING", "LANDSCAPE_IRRIGATION", "LANDSCAPE_PLAYGROUND"],
            "Пусконаладка": ["COMMISSIONING_ELECTRIC", "COMMISSIONING_PLUMBING", "COMMISSIONING_HVAC", "COMMISSIONING_AUTOMATION"],
            "Изоляционные": ["INSULATION_THERMAL", "INSULATION_WATER", "INSULATION_SOUND", "INSULATION_FIRE"],
            "Дорожные": ["ROAD_BASE", "ROAD_ASPHALT", "ROAD_CONCRETE", "ROAD_CURB", "ROAD_MARKING"],
            "Монолитные": ["MONOLITHIC_WALL", "MONOLITHIC_CEILING", "MONOLITHIC_STAIRS"],
            "Прочие": ["SCAFFOLDING", "CRANE_OPERATION", "WASTE_REMOVAL", "SNOW_CLEARING", "WATER_PUMPING"]
        }
        
        work_type_name = work_type.name if hasattr(work_type, 'name') else str(work_type)
        
        for category, items in categories.items():
            if work_type_name in items:
                return category
        return "Прочие"
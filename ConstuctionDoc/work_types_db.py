from models import WorkType

WORK_CATEGORIES = {
    "1. Подготовительные работы": [
        WorkType.CLEARING_SITE, WorkType.DEMOLITION, WorkType.GEODESY,
        WorkType.SITE_PLANNING, WorkType.UTILITIES_RELOCATION
    ],
    "2. Земляные работы": [
        WorkType.EARTH_EXCAVATION, WorkType.EARTH_MANUAL, WorkType.EARTH_BACKFILL,
        WorkType.EARTH_COMPACTION, WorkType.EARTH_TRENCH, WorkType.EARTH_PIT,
        WorkType.EARTH_IMPORT, WorkType.EARTH_EXPORT
    ],
    "3. Свайные работы": [
        WorkType.PILE_DRIVING, WorkType.PILE_BORED, WorkType.PILE_SCREW, WorkType.PILE_GROUTING
    ],
    "4. Фундаментные работы": [
        WorkType.FOUNDATION_BLOCK, WorkType.FOUNDATION_MONOLITHIC, WorkType.FOUNDATION_STRIP,
        WorkType.FOUNDATION_SLAB, WorkType.FOUNDATION_COLUMN, WorkType.FOUNDATION_WATERPROOFING,
        WorkType.FOUNDATION_INSULATION
    ],
    "5. Бетонные работы": [
        WorkType.CONCRETE_PREPARATION, WorkType.CONCRETE_FORMWORK, WorkType.CONCRETE_REINFORCEMENT,
        WorkType.CONCRETE_POURING, WorkType.CONCRETE_VIBRATION, WorkType.CONCRETE_CURING,
        WorkType.CONCRETE_STRIPPING, WorkType.CONCRETE_GROUTING
    ],
    "6. Каменные работы": [
        WorkType.MASONRY_BRICK, WorkType.MASONRY_BLOCK, WorkType.MASONRY_SILICATE,
        WorkType.MASONRY_PARTITION, WorkType.MASONRY_REINFORCED, WorkType.MASONRY_FACING
    ],
    "7. Монтажные работы": [
        WorkType.INSTALLATION_COLUMN, WorkType.INSTALLATION_BEAM, WorkType.INSTALLATION_SLAB,
        WorkType.INSTALLATION_TRUSS, WorkType.INSTALLATION_METAL, WorkType.INSTALLATION_CRANE,
        WorkType.INSTALLATION_LIFT, WorkType.INSTALLATION_STAIRS, WorkType.INSTALLATION_WINDOWS,
        WorkType.INSTALLATION_DOORS, WorkType.INSTALLATION_VENTILATION
    ],
    "8. Кровельные работы": [
        WorkType.ROOF_RAFTER, WorkType.ROOF_SHEATHING, WorkType.ROOF_COUNTER,
        WorkType.ROOF_VAPOR_BARRIER, WorkType.ROOF_INSULATION, WorkType.ROOF_UNDERLAYMENT,
        WorkType.ROOF_METAL, WorkType.ROOF_SOFT, WorkType.ROOF_FLAT, WorkType.ROOF_SEAM,
        WorkType.ROOF_COMPOSITE, WorkType.ROOF_DRAINAGE, WorkType.ROOF_SNOW_RETENTION
    ],
    "9. Отделочные работы": [
        WorkType.FINISHING_PLASTER, WorkType.FINISHING_PUTTY, WorkType.FINISHING_PAINT,
        WorkType.FINISHING_WALLPAPER, WorkType.FINISHING_TILE, WorkType.FINISHING_FLOOR_SCREED,
        WorkType.FINISHING_FLOOR, WorkType.FINISHING_CEILING, WorkType.FINISHING_SUSPENDED,
        WorkType.FINISHING_STRETCH, WorkType.FINISHING_DECORATIVE, WorkType.FINISHING_PANEL
    ],
    "10. Фасадные работы": [
        WorkType.FACADE_INSULATION, WorkType.FACADE_PLASTER, WorkType.FACADE_BRICK,
        WorkType.FACADE_VENTILATED, WorkType.FACADE_PANEL, WorkType.FACADE_PAINT,
        WorkType.FACADE_CLADDING
    ],
    "11. Сантехнические работы": [
        WorkType.PLUMBING_WATER, WorkType.PLUMBING_SEWER, WorkType.PLUMBING_HEATING,
        WorkType.PLUMBING_RADIATOR, WorkType.PLUMBING_FLOOR_HEATING, WorkType.PLUMBING_BOILER,
        WorkType.PLUMBING_EQUIPMENT, WorkType.PLUMBING_PUMP
    ],
    "12. Электромонтажные работы": [
        WorkType.ELECTRIC_CABLE, WorkType.ELECTRIC_PANEL, WorkType.ELECTRIC_LIGHTING,
        WorkType.ELECTRIC_GROUNDING, WorkType.ELECTRIC_AUTOMATION, WorkType.ELECTRIC_SOCKET,
        WorkType.ELECTRIC_WARM_FLOOR
    ],
    "13. Слаботочные системы": [
        WorkType.LOW_CURRENT_NETWORK, WorkType.LOW_CURRENT_SECURITY, WorkType.LOW_CURRENT_VIDEO,
        WorkType.LOW_CURRENT_INTERNET, WorkType.LOW_CURRENT_FIRE, WorkType.LOW_CURRENT_CONTROL
    ],
    "14. Вентиляция и кондиционирование": [
        WorkType.HVAC_DUCT, WorkType.HVAC_EQUIPMENT, WorkType.HVAC_INSULATION,
        WorkType.HVAC_GRILLE, WorkType.HVAC_SPLIT, WorkType.HVAC_VRV
    ],
    "15. Благоустройство": [
        WorkType.LANDSCAPE_PAVING, WorkType.LANDSCAPE_GREENING, WorkType.LANDSCAPE_FENCE,
        WorkType.LANDSCAPE_GATES, WorkType.LANDSCAPE_LIGHTING, WorkType.LANDSCAPE_IRRIGATION,
        WorkType.LANDSCAPE_PLAYGROUND
    ],
    "16. Пусконаладочные работы": [
        WorkType.COMMISSIONING_ELECTRIC, WorkType.COMMISSIONING_PLUMBING,
        WorkType.COMMISSIONING_HVAC, WorkType.COMMISSIONING_AUTOMATION
    ],
    "17. Изоляционные работы": [
        WorkType.INSULATION_THERMAL, WorkType.INSULATION_WATER,
        WorkType.INSULATION_SOUND, WorkType.INSULATION_FIRE
    ],
    "18. Дорожные работы": [
        WorkType.ROAD_BASE, WorkType.ROAD_ASPHALT, WorkType.ROAD_CONCRETE,
        WorkType.ROAD_CURB, WorkType.ROAD_MARKING
    ],
    "19. Монолитные работы": [
        WorkType.MONOLITHIC_WALL, WorkType.MONOLITHIC_CEILING, WorkType.MONOLITHIC_STAIRS
    ],
    "20. Прочие работы": [
        WorkType.SCAFFOLDING, WorkType.CRANE_OPERATION, WorkType.WASTE_REMOVAL,
        WorkType.SNOW_CLEARING, WorkType.WATER_PUMPING
    ],
}

def get_all_work_types():
    all_works = []
    for category, works in WORK_CATEGORIES.items():
        for work in works:
            all_works.append({
                "category": category,
                "work_type": work,
                "value": work.value
            })
    return all_works

def get_work_categories():
    return list(WORK_CATEGORIES.keys())

def get_works_by_category(category):
    return WORK_CATEGORIES.get(category, [])
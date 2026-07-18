# alpha/engine/scoring/data.py
from .models import Company, Financials, Multipliers

# ============================================
# VSYDP — Выборгский судостроительный завод
# ============================================
VSYDP_COMPANY = Company(
    ticker='VSYDP',
    name='Выборгский судостроительный завод',
    sector='Машиностроение',
    industry='Судостроение',
    isin='RU000A0B8GZ1',
    lot_size=1,
    free_float=0.15
)

VSYDP_FINANCIALS = Financials(
    ticker='VSYDP',
    revenue=11_100_000_000,
    ebitda=1_500_000_000,
    net_income=142_000_000,
    total_assets=12_000_000_000,
    total_equity=500_000_000,
    total_debt=3_000_000_000,
    cash=500_000_000,
    operating_cash_flow=300_000_000,
    capex=100_000_000,
)

VSYDP_MULTIPLIERS = Multipliers(
    ticker='VSYDP',
    price=42000,
    market_cap=2_175_600_000,
    pe=15.3,
    pb=4.35,
    ps=0.2,
    ev_ebitda=4.5,
    dividend_yield=0.0,
)

# ============================================
# GCHE — Группа Черкизово
# ============================================
GCHE_COMPANY = Company(
    ticker='GCHE',
    name='Группа Черкизово',
    sector='Пищевая промышленность',
    industry='Мясопереработка',
    isin='RU000A0JL4R1',
    lot_size=1,
    free_float=0.35
)

GCHE_FINANCIALS = Financials(
    ticker='GCHE',
    revenue=250_000_000_000,
    ebitda=45_000_000_000,
    net_income=22_000_000_000,
    total_assets=180_000_000_000,
    total_equity=80_000_000_000,
    total_debt=60_000_000_000,
    cash=15_000_000_000,
    operating_cash_flow=30_000_000_000,
    capex=8_000_000_000,
)

GCHE_MULTIPLIERS = Multipliers(
    ticker='GCHE',
    price=5400,
    market_cap=220_000_000_000,
    pe=10.0,
    pb=2.75,
    ps=0.88,
    ev_ebitda=5.8,
    dividend_yield=4.5,
)

# ============================================
# NVTK — НОВАТЭК
# ============================================
NVTK_COMPANY = Company(
    ticker='NVTK',
    name='НОВАТЭК',
    sector='Нефть и газ',
    industry='Газовая промышленность',
    isin='RU000A0DKVS5',
    lot_size=1,
    free_float=0.42
)

NVTK_FINANCIALS = Financials(
    ticker='NVTK',
    revenue=1_500_000_000_000,
    ebitda=500_000_000_000,
    net_income=350_000_000_000,
    total_assets=2_200_000_000_000,
    total_equity=1_400_000_000_000,
    total_debt=400_000_000_000,
    cash=200_000_000_000,
    operating_cash_flow=450_000_000_000,
    capex=120_000_000_000,
)

NVTK_MULTIPLIERS = Multipliers(
    ticker='NVTK',
    price=920,
    market_cap=2_800_000_000_000,
    pe=8.0,
    pb=2.0,
    ps=1.87,
    ev_ebitda=5.2,
    dividend_yield=6.8,
)

# ============================================
# CHMF — Северсталь
# ============================================
CHMF_COMPANY = Company(
    ticker='CHMF',
    name='Северсталь',
    sector='Металлургия',
    industry='Чёрная металлургия',
    isin='RU000A0DKVS5',
    lot_size=1,
    free_float=0.28
)

CHMF_FINANCIALS = Financials(
    ticker='CHMF',
    revenue=850_000_000_000,
    ebitda=220_000_000_000,
    net_income=140_000_000_000,
    total_assets=700_000_000_000,
    total_equity=350_000_000_000,
    total_debt=120_000_000_000,
    cash=80_000_000_000,
    operating_cash_flow=180_000_000_000,
    capex=45_000_000_000,
)

CHMF_MULTIPLIERS = Multipliers(
    ticker='CHMF',
    price=1450,
    market_cap=1_100_000_000_000,
    pe=7.9,
    pb=3.14,
    ps=1.29,
    ev_ebitda=4.5,
    dividend_yield=8.2,
)
# ============================================
# Реальные данные для 14 акций (2024–2025)
# ============================================

# SBER — Сбербанк
REAL_SBER_FINANCIALS = Financials(
    ticker='SBER',
    revenue=3_200_000_000_000,    # 3.2 трлн руб.
    ebitda=1_800_000_000_000,
    net_income=1_500_000_000_000,
    total_assets=45_000_000_000_000,
    total_equity=5_500_000_000_000,
    total_debt=1_200_000_000_000,
    cash=800_000_000_000,
    operating_cash_flow=1_600_000_000_000,
    capex=200_000_000_000,
)

# GAZP — Газпром
REAL_GAZP_FINANCIALS = Financials(
    ticker='GAZP',
    revenue=8_500_000_000_000,
    ebitda=2_200_000_000_000,
    net_income=1_100_000_000_000,
    total_assets=25_000_000_000_000,
    total_equity=12_000_000_000_000,
    total_debt=4_500_000_000_000,
    cash=1_200_000_000_000,
    operating_cash_flow=2_000_000_000_000,
    capex=1_800_000_000_000,
)

# LKOH — Лукойл
REAL_LKOH_FINANCIALS = Financials(
    ticker='LKOH',
    revenue=7_800_000_000_000,
    ebitda=1_600_000_000_000,
    net_income=1_200_000_000_000,
    total_assets=8_500_000_000_000,
    total_equity=5_200_000_000_000,
    total_debt=1_100_000_000_000,
    cash=500_000_000_000,
    operating_cash_flow=1_500_000_000_000,
    capex=700_000_000_000,
)

# NVTK — НОВАТЭК
REAL_NVTK_FINANCIALS = Financials(
    ticker='NVTK',
    revenue=1_600_000_000_000,
    ebitda=550_000_000_000,
    net_income=380_000_000_000,
    total_assets=2_400_000_000_000,
    total_equity=1_600_000_000_000,
    total_debt=450_000_000_000,
    cash=220_000_000_000,
    operating_cash_flow=480_000_000_000,
    capex=150_000_000_000,
)

# CHMF — Северсталь
REAL_CHMF_FINANCIALS = Financials(
    ticker='CHMF',
    revenue=850_000_000_000,
    ebitda=220_000_000_000,
    net_income=140_000_000_000,
    total_assets=700_000_000_000,
    total_equity=380_000_000_000,
    total_debt=120_000_000_000,
    cash=80_000_000_000,
    operating_cash_flow=200_000_000_000,
    capex=50_000_000_000,
)

# MGNT — Магнит
REAL_MGNT_FINANCIALS = Financials(
    ticker='MGNT',
    revenue=2_800_000_000_000,
    ebitda=280_000_000_000,
    net_income=120_000_000_000,
    total_assets=1_200_000_000_000,
    total_equity=400_000_000_000,
    total_debt=500_000_000_000,
    cash=80_000_000_000,
    operating_cash_flow=250_000_000_000,
    capex=120_000_000_000,
)

# TATN — Татнефть
REAL_TATN_FINANCIALS = Financials(
    ticker='TATN',
    revenue=1_400_000_000_000,
    ebitda=350_000_000_000,
    net_income=250_000_000_000,
    total_assets=1_800_000_000_000,
    total_equity=1_200_000_000_000,
    total_debt=200_000_000_000,
    cash=150_000_000_000,
    operating_cash_flow=320_000_000_000,
    capex=100_000_000_000,
)

# ROSN — Роснефть
REAL_ROSN_FINANCIALS = Financials(
    ticker='ROSN',
    revenue=9_000_000_000_000,
    ebitda=2_000_000_000_000,
    net_income=1_300_000_000_000,
    total_assets=18_000_000_000_000,
    total_equity=8_000_000_000_000,
    total_debt=4_000_000_000_000,
    cash=800_000_000_000,
    operating_cash_flow=1_800_000_000_000,
    capex=1_000_000_000_000,
)

# PLZL — Полюс
REAL_PLZL_FINANCIALS = Financials(
    ticker='PLZL',
    revenue=250_000_000_000,
    ebitda=120_000_000_000,
    net_income=80_000_000_000,
    total_assets=500_000_000_000,
    total_equity=300_000_000_000,
    total_debt=80_000_000_000,
    cash=40_000_000_000,
    operating_cash_flow=100_000_000_000,
    capex=60_000_000_000,
)

# YDEX — Яндекс (данные за 2024 год)
REAL_YDEX_FINANCIALS = Financials(
    ticker='YDEX',
    revenue=1_100_000_000_000,
    ebitda=180_000_000_000,
    net_income=70_000_000_000,
    total_assets=900_000_000_000,
    total_equity=300_000_000_000,
    total_debt=250_000_000_000,
    cash=150_000_000_000,
    operating_cash_flow=160_000_000_000,
    capex=80_000_000_000,
)

# MOEX — Мосбиржа
REAL_MOEX_FINANCIALS = Financials(
    ticker='MOEX',
    revenue=90_000_000_000,
    ebitda=50_000_000_000,
    net_income=35_000_000_000,
    total_assets=500_000_000_000,
    total_equity=120_000_000_000,
    total_debt=0,
    cash=50_000_000_000,
    operating_cash_flow=45_000_000_000,
    capex=5_000_000_000,
)

# ============================================
# Реальные финансовые данные для всех акций
# ============================================

# SBERP — Сбербанк-пр (те же данные, что у Сбербанка)
REAL_SBERP_FINANCIALS = Financials(
    ticker='SBERP',
    revenue=3_200_000_000_000,
    ebitda=1_800_000_000_000,
    net_income=1_500_000_000_000,
    total_assets=45_000_000_000_000,
    total_equity=5_500_000_000_000,
    total_debt=1_200_000_000_000,
    cash=800_000_000_000,
    operating_cash_flow=1_600_000_000_000,
    capex=200_000_000_000,
)

# VTBR — ВТБ
REAL_VTBR_FINANCIALS = Financials(
    ticker='VTBR',
    revenue=1_500_000_000_000,
    ebitda=600_000_000_000,
    net_income=400_000_000_000,
    total_assets=30_000_000_000_000,
    total_equity=2_500_000_000_000,
    total_debt=800_000_000_000,
    cash=400_000_000_000,
    operating_cash_flow=500_000_000_000,
    capex=100_000_000_000,
)

# GCHE — Группа Черкизово (уже есть, но добавим для полноты)
REAL_GCHE_FINANCIALS = Financials(
    ticker='GCHE',
    revenue=250_000_000_000,
    ebitda=45_000_000_000,
    net_income=22_000_000_000,
    total_assets=180_000_000_000,
    total_equity=80_000_000_000,
    total_debt=60_000_000_000,
    cash=15_000_000_000,
    operating_cash_flow=30_000_000_000,
    capex=8_000_000_000,
)
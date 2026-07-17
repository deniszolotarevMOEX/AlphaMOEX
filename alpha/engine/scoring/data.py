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
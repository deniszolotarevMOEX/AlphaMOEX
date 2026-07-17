# alpha/engine/scoring/models.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Company:
    """Модель компании"""
    ticker: str
    name: str
    sector: str
    industry: Optional[str] = None
    isin: Optional[str] = None
    lot_size: int = 1
    free_float: float = 0.0

@dataclass
class Financials:
    """Финансовые показатели компании"""
    ticker: str
    revenue: float = 0.0          # Выручка
    ebitda: float = 0.0           # EBITDA
    net_income: float = 0.0       # Чистая прибыль
    total_assets: float = 0.0     # Активы
    total_equity: float = 0.0     # Капитал
    total_debt: float = 0.0       # Долг
    cash: float = 0.0             # Денежные средства
    operating_cash_flow: float = 0.0
    capex: float = 0.0

@dataclass
class Multipliers:
    """Рыночные мультипликаторы"""
    ticker: str
    price: float = 0.0
    market_cap: float = 0.0
    pe: Optional[float] = None
    pb: Optional[float] = None
    ps: Optional[float] = None
    ev_ebitda: Optional[float] = None
    dividend_yield: Optional[float] = None
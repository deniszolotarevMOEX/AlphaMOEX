# alpha/engine/scoring/scorer.py
from typing import Dict, List, Optional
from .models import Company, Financials, Multipliers

class KlechevScorer:
    """
    Индекс Клещёва — оценка инвестиционной привлекательности акций.
    Рейтинг от 0 до 1000 баллов.
    """
   
    def __init__(self):
        self.weights = {
            'quality': 0.20,
            'stability': 0.15,
            'undervaluation': 0.25,
            'growth': 0.10,
            'cash_flow': 0.10,
            'equity': 0.05,
            'inefficiency': 0.10,
            'catalysts': 0.05,
        }
   
    def score_company(
        self,
        company: Company,
        financials: Financials,
        multipliers: Multipliers,
        peers: Optional[List[dict]] = None
    ) -> Dict:
        """Рассчитывает рейтинг для одной компании."""
       
        quality_score = self._calculate_quality(financials)
        stability_score = self._calculate_stability(financials)
        undervaluation_score = self._calculate_undervaluation(multipliers)
        growth_score = self._calculate_growth(financials)
        cash_flow_score = self._calculate_cash_flow(financials)
        equity_score = self._calculate_equity(company, financials)
        inefficiency_score = self._calculate_inefficiency(company, multipliers)
        catalysts_score = self._calculate_catalysts(company, financials)
       
        total_score = (
            quality_score * self.weights['quality'] +
            stability_score * self.weights['stability'] +
            undervaluation_score * self.weights['undervaluation'] +
            growth_score * self.weights['growth'] +
            cash_flow_score * self.weights['cash_flow'] +
            equity_score * self.weights['equity'] +
            inefficiency_score * self.weights['inefficiency'] +
            catalysts_score * self.weights['catalysts']
        )
       
        return {
            'total': round(total_score, 1),
            'quality': round(quality_score, 1),
            'stability': round(stability_score, 1),
            'undervaluation': round(undervaluation_score, 1),
            'growth': round(growth_score, 1),
            'cash_flow': round(cash_flow_score, 1),
            'equity': round(equity_score, 1),
            'inefficiency': round(inefficiency_score, 1),
            'catalysts': round(catalysts_score, 1),
            'grade': self._get_grade(total_score),
        }
   
    def _calculate_quality(self, fin: Financials) -> float:
        score = 0.0
        if fin.total_equity > 0:
            roe = fin.net_income / fin.total_equity
            if roe > 0.30: score += 40
            elif roe > 0.20: score += 35
            elif roe > 0.15: score += 30
            elif roe > 0.10: score += 20
            elif roe > 0.05: score += 10
            else: score += 5
        if fin.total_assets > 0:
            roic = fin.ebitda / fin.total_assets
            if roic > 0.25: score += 40
            elif roic > 0.20: score += 35
            elif roic > 0.15: score += 30
            elif roic > 0.10: score += 20
            else: score += 10
        if fin.revenue > 0:
            margin = fin.ebitda / fin.revenue
            if margin > 0.30: score += 20
            elif margin > 0.20: score += 15
            elif margin > 0.10: score += 10
            else: score += 5
        return min(score, 200)
   
    def _calculate_stability(self, fin: Financials) -> float:
        score = 0.0
        if fin.ebitda > 0:
            debt_ebitda = fin.total_debt / fin.ebitda
            if debt_ebitda < 0.5: score += 50
            elif debt_ebitda < 1.0: score += 40
            elif debt_ebitda < 2.0: score += 30
            elif debt_ebitda < 3.0: score += 20
            else: score += 10
        if fin.total_debt > 0:
            cash_debt = fin.cash / fin.total_debt
            if cash_debt > 1.0: score += 50
            elif cash_debt > 0.5: score += 40
            elif cash_debt > 0.2: score += 30
            else: score += 20
        elif fin.total_debt == 0:
            score += 50
        return min(score, 150)
   
    def _calculate_undervaluation(self, mul: Multipliers) -> float:
        score = 0.0
        if mul.pe and mul.pe > 0:
            if mul.pe < 5: score += 60
            elif mul.pe < 8: score += 50
            elif mul.pe < 12: score += 40
            elif mul.pe < 15: score += 30
            elif mul.pe < 20: score += 20
            else: score += 10
        if mul.pb and mul.pb > 0:
            if mul.pb < 0.5: score += 50
            elif mul.pb < 1.0: score += 40
            elif mul.pb < 1.5: score += 30
            elif mul.pb < 2.0: score += 20
            else: score += 10
        if mul.ev_ebitda and mul.ev_ebitda > 0:
            if mul.ev_ebitda < 3: score += 60
            elif mul.ev_ebitda < 5: score += 50
            elif mul.ev_ebitda < 8: score += 40
            elif mul.ev_ebitda < 12: score += 30
            else: score += 20
        return min(score, 250)
   
    def _calculate_growth(self, fin: Financials) -> float:
        return 50.0
   
    def _calculate_cash_flow(self, fin: Financials) -> float:
        score = 0.0
        fcf = fin.operating_cash_flow - fin.capex
        if fcf > 0: score += 50
        if fin.revenue > 0:
            fcf_margin = fcf / fin.revenue
            if fcf_margin > 0.15: score += 50
            elif fcf_margin > 0.10: score += 40
            elif fcf_margin > 0.05: score += 30
            else: score += 15
        return min(score, 100)
   
    def _calculate_equity(self, company: Company, fin: Financials) -> float:
        return 40.0
   
    def _calculate_inefficiency(self, company: Company, mul: Multipliers) -> float:
        score = 0.0
        if mul.market_cap and mul.market_cap < 10_000_000_000:
            score += 20
        if company.free_float and company.free_float < 0.25:
            score += 20
        if mul.market_cap and mul.market_cap < 50_000_000_000:
            score += 20
        score += 20
        return min(score, 100)
   
    def _calculate_catalysts(self, company: Company, fin: Financials) -> float:
        return 30.0
   
    def _get_grade(self, score: float) -> str:
        if score >= 900: return "A+"
        elif score >= 800: return "A"
        elif score >= 700: return "B"
        elif score >= 600: return "C"
        else: return "D"
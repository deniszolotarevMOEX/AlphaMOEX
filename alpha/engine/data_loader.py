# alpha/engine/data_loader.py
import logging
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional 

logger = logging.getLogger(__name__)


class MoexDataLoader:
    """Загрузчик данных через MOEX ISS API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'AlphaMOEX/0.1'})
    
    def get_all_shares(self) -> List[Dict]:
        """
        Загружает ВСЕ акции с Московской биржи через MOEX API.
        """
        all_securities = []
        
        try:
            url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
            params = {
                'iss.meta': 'off',
                'limit': 300,  # Увеличиваем лимит, чтобы получить больше акций за один раз
            }
            
            # Увеличиваем таймаут до 30 секунд
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get('securities', {}).get('data', []):
                if len(item) < 6:
                    continue
                
                ticker = item[0]
                name = item[1] if len(item) > 1 else ticker
                sec_type = item[3] if len(item) > 3 else ''
                status = item[4] if len(item) > 4 else ''
                
                # Фильтруем: только акции, которые торгуются
                if sec_type not in ['common', 'preferred']:
                    continue
                if status != 'T':
                    continue
                
                all_securities.append({
                    'ticker': ticker,
                    'name': name,
                    'isin': item[2] if len(item) > 2 else '',
                    'sec_type': sec_type,
                    'shares_outstanding': 0,
                })
            
            logger.info(f"Загружено {len(all_securities)} акций через MOEX API")
            
        except Exception as e:
            logger.error(f"Ошибка загрузки списка акций: {e}")
            # Если API не работает — возвращаем пустой список
        
        return all_securities
    
    def _get_company_names(self, tickers: List[str]) -> Dict[str, str]:
        """Возвращает правильные названия компаний из справочника"""
        # Полный справочник названий для всех тикеров
        names_dict = {
            # Банки и финансы
            'SBER': 'Сбербанк',
            'SBERP': 'Сбербанк-пр',
            'VTBR': 'ВТБ',
            'MOEX': 'Московская биржа',
            'AFKS': 'АФК Система',
            'CBOM': 'МКБ',
            
            # Нефть и газ
            'GAZP': 'Газпром',
            'LKOH': 'Лукойл',
            'ROSN': 'Роснефть',
            'NVTK': 'НОВАТЭК',
            'TATN': 'Татнефть',
            'SIBN': 'Газпром нефть',
            'SNGSP': 'Сургутнефтегаз-пр',
            'TRNFP': 'Транснефть-пр',
            'BANE': 'Башнефть',
            
            # Металлургия и горнодобыча
            'CHMF': 'Северсталь',
            'MAGN': 'ММК',
            'NLMK': 'НЛМК',
            'ALRS': 'АЛРОСА',
            'PLZL': 'Полюс',
            'RUAL': 'РУСАЛ',
            'URKA': 'Уралкалий',
            'PHOR': 'ФосАгро',
            
            # Ритейл и потребительский сектор
            'MGNT': 'Магнит',
            'FIVE': 'X5 Group',
            'FIXP': 'Fix Price',
            'OZON': 'Ozon',
            'LENT': 'Лента',
            
            # IT и телеком
            'YDEX': 'Яндекс',
            'VKCO': 'VK',
            'MTSS': 'МТС',
            'AFLT': 'Аэрофлот',
            
            # Энергетика
            'IRAO': 'Интер РАО',
            'FEES': 'ФСК ЕЭС',
            'HYDR': 'РусГидро',
            'TGKA': 'ТГК-1',
            'OGKB': 'ОГК-2',
            'UNAC': 'Юнипро',
            'UPRO': 'Россети',
            'UFGS': 'Россети-Кубань',
            
            # Машиностроение и другие
            'TRMK': 'ТМК',
            'TTLK': 'Таттелеком',
            'VSMO': 'ВСМПО-АВИСМА',
            'WTCM': 'Московский метрополитен',
            'ZVEZ': 'Звезда',
            'HALS': 'Галс-Девелопмент',
            'IRKT': 'Иркут',
            'KMAZ': 'КАМАЗ',
            'SELG': 'Сегежа',
            'SGZH': 'Совкомфлот',
            'TASR': 'ТВЭЛ',
            'TORSP': 'Торговый дом ТМК',
            'GCHE': 'Группа Черкизово',
        }
        
        # Возвращаем названия только для запрошенных тикеров
        return {ticker: names_dict.get(ticker, ticker) for ticker in tickers}
    
    def _get_fallback_companies(self) -> List[Dict]:
        """
        Фиксированный список акций (если API не работает).
        """
        print("🔄 Используем фиксированный список акций (49 тикеров)")
        
        tickers = [
            'SBER', 'SBERP', 'VTBR', 'GAZP', 'LKOH', 'NVTK', 'GCHE',
            'CHMF', 'MGNT', 'TATN', 'ROSN', 'PLZL', 'YDEX', 'MOEX',
            'MTSS', 'AFLT', 'RUAL', 'ALRS', 'IRAO', 'FEES', 'HYDR',
            'MAGN', 'NLMK', 'URKA', 'PHOR', 'TRNFP', 'FIVE', 'FIXP',
            'OZON', 'VKCO', 'AFKS', 'SELG', 'SGZH', 'SIBN', 'SNGSP',
            'TASR', 'TGKA', 'TORSP', 'TRMK', 'TTLK', 'UFGS', 'UNAC',
            'UPRO', 'VSMO', 'WTCM', 'ZVEZ', 'HALS', 'IRKT', 'KMAZ',
        ]
        
        names = self._get_company_names(tickers)
        
        companies = []
        for ticker in tickers:
            companies.append({
                'ticker': ticker,
                'name': names.get(ticker, ticker),
                'isin': '',
                'sec_type': 'common',
                'shares_outstanding': 0,
            })
        
        print(f"✅ Загружено {len(companies)} акций (фиксированный список)")
        return companies
    
    def get_current_prices(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Загружает цены и мультипликаторы (P/E, P/B) через MOEX API.
        """
        if not tickers:
            return {}
        
        result = {}
        
        try:
            url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
            params = {

                'iss.meta': 'off',
                'limit': 100,
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Собираем данные из блоков securities и marketdata
            # Сначала создаём словарь для быстрого доступа
            for row in data.get('marketdata', {}).get('data', []):
                if len(row) >= 20:  # В marketdata много полей
                    ticker = row[0]
                    price = row[2] if len(row) > 2 else None
                    pe = row[15] if len(row) > 15 else None   # P/E
                    pb = row[16] if len(row) > 16 else None   # P/B
                    # Нормализуем P/B (делим на 100, так как API выдаёт в копейках)
                    if pb:
                        pb = pb / 100.0
                    
                    if ticker in tickers and price:
                        result[ticker] = {
                            'price': float(price),
                            'pe': float(pe) if pe else None,
                            'pb': float(pb) if pb else None,
                            'market_cap': 0,
                            'volume': 0,
                        }
            
            logger.info(f"Загружены цены и мультипликаторы для {len(result)} акций")
            
        except Exception as e:
            logger.error(f"Ошибка загрузки данных: {e}")
            # Если ошибка — возвращаем тестовые цены
            for ticker in tickers:
                result[ticker] = {'price': 100.0, 'pe': None, 'pb': None, 'market_cap': 0, 'volume': 0}
        
        return result
    
    def _get_fallback_prices(self, tickers: List[str]) -> Dict[str, Dict]:
        """Тестовые цены, если API недоступен"""
        logger.warning("Используем тестовые цены")
        test_prices = {
            'SBER': 250, 'SBERP': 230, 'VTBR': 0.02, 'GAZP': 160,
            'LKOH': 7000, 'NVTK': 1300, 'GCHE': 5400, 'CHMF': 1600,
            'MGNT': 4500, 'TATN': 650, 'ROSN': 500, 'PLZL': 10000,
            'YDEX': 4000, 'MOEX': 130,  # Яндекс теперь YDEX, а не YNDX
            'MTSS': 250, 'AFLT': 40, 'RUAL': 40, 'ALRS': 80,
            'IRAO': 4, 'FEES': 0.1, 'HYDR': 0.8, 'MAGN': 50,
            'NLMK': 150, 'URKA': 200, 'PHOR': 300, 'TRNFP': 800,
            'FIVE': 2500, 'FIXP': 250, 'OZON': 3000, 'VKCO': 500,
            'AFKS': 15, 'SELG': 80, 'SGZH': 300, 'SIBN': 500,
            'SNGSP': 40, 'TASR': 0.5, 'TGKA': 0.01, 'TORSP': 2,
            'TRMK': 80, 'TTLK': 100, 'UFGS': 5, 'UNAC': 50,
            'UPRO': 10, 'VSMO': 200, 'WTCM': 10, 'ZVEZ': 30,
            'HALS': 200, 'IRKT': 5, 'KMAZ': 150,
        }
        return {
            ticker: {'price': test_prices.get(ticker, 100), 'market_cap': 0, 'volume': 0}
            for ticker in tickers
        }

    def get_shares_outstanding(self, ticker: str) -> int:
        """
        Получает количество акций из справочника (если есть) или из API.
        """
        # Справочник для популярных акций (основные 50)
        shares_dict = {
            'SBER': 21_500_000_000,
            'SBERP': 21_500_000_000,
            'VTBR': 120_000_000_000,
            'GAZP': 23_600_000_000,
            'LKOH': 650_000_000,
            'NVTK': 3_000_000_000,
            'GCHE': 43_000_000,
            'CHMF': 840_000_000,
            'MGNT': 270_000_000,
            'TATN': 2_100_000_000,
            'ROSN': 10_600_000_000,
            'PLZL': 130_000_000,
            'YDEX': 360_000_000,
            'MOEX': 225_000_000,
            'MTSS': 1_500_000_000,
            'AFLT': 2_000_000_000,
            'RUAL': 15_000_000_000,
            'ALRS': 7_000_000_000,
            'IRAO': 30_000_000_000,
            'FEES': 400_000_000_000,
            'HYDR': 40_000_000_000,
            'MAGN': 10_000_000_000,
            'NLMK': 6_000_000_000,
            'URKA': 3_000_000_000,
            'PHOR': 130_000_000,
            'TRNFP': 1_000_000_000,
            'FIVE': 270_000_000,
            'FIXP': 270_000_000,
            'OZON': 100_000_000,
            'VKCO': 200_000_000,
            'AFKS': 10_000_000_000,
            'SELG': 1_000_000_000,
            'SGZH': 1_000_000_000,
            'SIBN': 5_000_000_000,
            'SNGSP': 10_000_000_000,
            'TASR': 1_000_000_000,
            'TGKA': 50_000_000_000,
            'TORSP': 1_000_000_000,
            'TRMK': 1_000_000_000,
            'TTLK': 1_000_000_000,
            'UFGS': 1_000_000_000,
            'UNAC': 1_000_000_000,
            'UPRO': 1_000_000_000,
            'VSMO': 1_000_000_000,
            'WTCM': 1_000_000_000,
            'ZVEZ': 1_000_000_000,
            'HALS': 1_000_000_000,
            'IRKT': 1_000_000_000,
            'KMAZ': 1_000_000_000,
        }
        
        # 1. Сначала проверяем справочник
        if ticker in shares_dict:
            return shares_dict[ticker]
        
        # 2. Если нет в справочнике — пробуем API
        try:
            url = f"https://iss.moex.com/iss/securities/{ticker}.json"
            params = {'iss.meta': 'off'}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'securities' in data and 'data' in data['securities']:
                for row in data['securities']['data']:
                    if len(row) > 1 and row[0] == ticker:
                        issued = row[5] if len(row) > 5 else None
                        if issued:
                            return int(issued)
            return 0
        except Exception as e:
            logger.warning(f"Не удалось получить количество акций для {ticker}: {e}")
            return 0
    def get_total_equity(self, ticker: str) -> float:
        """
        Получает балансовую стоимость (Total Equity) компании из MOEX API.
        Использует данные из отчётности.
        """
        url = f"https://iss.moex.com/iss/securities/{ticker}/financials.json"
        params = {
            'iss.meta': 'off',
            'limit': 1,
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Ищем показатель "Total Equity" или "Capital and Reserves"
            if 'financials' in data and 'data' in data['financials']:
                for row in data['financials']['data']:
                    if len(row) >= 3:
                        # Ищем строку с "Total Equity"
                        if 'Total Equity' in row[0] or 'Capital and Reserves' in row[0]:
                            return float(row[2]) if row[2] else 0.0
            return 0.0
        except Exception as e:
            logger.warning(f"Не удалось получить балансовую стоимость для {ticker}: {e}")
            return 0.0  

    def load_companies_cache(self) -> List[Dict]:
        """
        Загружает ВСЕ акции напрямую из API.
        """
        print("🔄 Загружаем список акций из API...")
        
        try:
            url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
            params = {
                'iss.meta': 'off',
                'limit': 500,
            }
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            companies = []
            for row in data.get('securities', {}).get('data', []):
                if len(row) < 25:
                    continue
                
                ticker = row[0]
                name = row[2]
                sec_type = row[24]
                status = row[6]
                isin = row[19] if len(row) > 19 else ''
                
                # ==========================================
                # ФИЛЬТР: только акции (SECTYPE=1), активные (STATUS=A)
                # ==========================================
                if sec_type != '1':      # Только акции (не ETF, не облигации)
                    continue
                if status != 'A':        # Только активные
                    continue
                
                companies.append({
                    'ticker': ticker,
                    'name': name,
                    'isin': isin,
                    'sec_type': sec_type,
                    'shares_outstanding': 0,
                })
            
            print(f"✅ Загружено {len(companies)} акций из API")
            
            if companies:
                print("📊 Примеры загруженных акций (первые 5):")
                for c in companies[:5]:
                    print(f"   {c['ticker']} - {c['name']}")
            
            return companies
            
        except Exception as e:
            print(f"❌ Ошибка загрузки из API: {e}")
            return self._get_fallback_companies()
    
    def _get_fallback_companies(self) -> List[Dict]:
        """
        Фиксированный список акций (если API не работает).
        """
        print("🔄 Используем фиксированный список акций (49 тикеров)")
        
        tickers = [
            'SBER', 'SBERP', 'VTBR', 'GAZP', 'LKOH', 'NVTK', 'GCHE',
            'CHMF', 'MGNT', 'TATN', 'ROSN', 'PLZL', 'YDEX', 'MOEX',
            'MTSS', 'AFLT', 'RUAL', 'ALRS', 'IRAO', 'FEES', 'HYDR',
            'MAGN', 'NLMK', 'URKA', 'PHOR', 'TRNFP', 'FIVE', 'FIXP',
            'OZON', 'VKCO', 'AFKS', 'SELG', 'SGZH', 'SIBN', 'SNGSP',
            'TASR', 'TGKA', 'TORSP', 'TRMK', 'TTLK', 'UFGS', 'UNAC',
            'UPRO', 'VSMO', 'WTCM', 'ZVEZ', 'HALS', 'IRKT', 'KMAZ',
        ]
        
        names = self._get_company_names(tickers)
        
        companies = []
        for ticker in tickers:
            companies.append({
                'ticker': ticker,
                'name': names.get(ticker, ticker),
                'isin': '',
                'sec_type': 'common',
                'shares_outstanding': 0,
            })
        
        print(f"✅ Загружено {len(companies)} акций (фиксированный список)")
        return companies
    
    def get_net_income(self, ticker: str) -> float:
        """
        Получает чистую прибыль из API MOEX (с диагностикой).
        """
        url = f"https://iss.moex.com/iss/securities/{ticker}/financials.json"
        params = {'iss.meta': 'off', 'limit': 1}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Диагностика: для первых 5 тикеров показываем структуру
            if ticker in ['AFLT', 'MTSS', 'RUAL', 'ALRS', 'IRAO']:
                print(f"📊 Диагностика для {ticker}:")
                print(f"  Ключи: {list(data.keys())}")
                if 'financials' in data:
                    print(f"  Ключи в financials: {list(data['financials'].keys())}")
                    if 'data' in data['financials']:
                        rows = data['financials']['data']
                        print(f"  Количество строк: {len(rows)}")
                        if rows:
                            print(f"  Первая строка: {rows[0][:5] if len(rows[0]) >= 5 else rows[0]}")
            
            # Ищем прибыль
            if 'financials' in data and 'data' in data['financials']:
                for row in data['financials']['data']:
                    if len(row) >= 3:
                        name = row[0] if len(row) > 0 else ''
                        # Пробуем разные варианты
                        if 'Net Income' in name or 'Чистая прибыль' in name or 'Net profit' in name:
                            value = row[2] if len(row) > 2 and row[2] else 0.0
                            if value and float(value) != 0:
                                print(f"✅ Найдена прибыль для {ticker}: {value}")
                                return float(value)
            return 0.0
        except Exception as e:
            print(f"❌ Ошибка для {ticker}: {e}")
            return 0.0
    
    
    
class DataManager:
    """Менеджер данных"""
    
    def __init__(self):
        self.loader = MoexDataLoader()
        self.companies = []
        self.companies_cache = []  # Кэш всех компаний
    
    def refresh_all_data(self) -> Dict:
        """Обновляет данные: список акций, цены и мультипликаторы"""
        logger.info("Начинаем обновление данных...")
        
        # ==========================================
        # 1. ЗАГРУЖАЕМ СПИСОК АКЦИЙ
        # ==========================================
        all_companies = self.loader.load_companies_cache()
        if not all_companies:
            return {'status': 'error', 'message': 'Не удалось загрузить список акций'}
        
        securities = all_companies
        tickers = [s['ticker'] for s in securities]
        
        # ==========================================
        # 2. ЗАГРУЖАЕМ ЦЕНЫ И МУЛЬТИПЛИКАТОРЫ
        # ==========================================
        prices = self.loader.get_current_prices(tickers)
        
        # ==========================================
        # 3. ЗАГРУЖАЕМ ФИНАНСОВЫЕ ДАННЫЕ (из data.py)
        # ==========================================
        from ..engine.scoring.data import (
            REAL_SBER_FINANCIALS, REAL_SBERP_FINANCIALS, REAL_VTBR_FINANCIALS,
            REAL_GAZP_FINANCIALS, REAL_LKOH_FINANCIALS, REAL_NVTK_FINANCIALS,
            REAL_CHMF_FINANCIALS, REAL_MGNT_FINANCIALS, REAL_TATN_FINANCIALS,
            REAL_ROSN_FINANCIALS, REAL_PLZL_FINANCIALS, REAL_YDEX_FINANCIALS,
            REAL_MOEX_FINANCIALS, REAL_GCHE_FINANCIALS,
        )
        
        financials_map = {
            'SBER': REAL_SBER_FINANCIALS,
            'SBERP': REAL_SBERP_FINANCIALS,
            'VTBR': REAL_VTBR_FINANCIALS,
            'GAZP': REAL_GAZP_FINANCIALS,
            'LKOH': REAL_LKOH_FINANCIALS,
            'NVTK': REAL_NVTK_FINANCIALS,
            'GCHE': REAL_GCHE_FINANCIALS,
            'CHMF': REAL_CHMF_FINANCIALS,
            'MGNT': REAL_MGNT_FINANCIALS,
            'TATN': REAL_TATN_FINANCIALS,
            'ROSN': REAL_ROSN_FINANCIALS,
            'PLZL': REAL_PLZL_FINANCIALS,
            'YDEX': REAL_YDEX_FINANCIALS,
            'MOEX': REAL_MOEX_FINANCIALS,
        }
        
        # ==========================================
        # 4. ОБРАБАТЫВАЕМ КАЖДУЮ АКЦИЮ
        # ==========================================
        result = []
        net_income_count = 0
        
        for sec in securities:
            ticker = sec['ticker']
            price_info = prices.get(ticker, {'price': 0})
            price = price_info.get('price', 0)
            
            # --- Количество акций ---
            shares = self.loader.get_shares_outstanding(ticker)
            
            # --- Балансовая стоимость ---
            total_equity = 0.0
            fin = financials_map.get(ticker)
            if fin and fin.total_equity > 0:
                total_equity = fin.total_equity
            else:
                total_equity = self.loader.get_total_equity(ticker)
            
            # --- Чистая прибыль ---
            net_income = 0.0
            if fin and fin.net_income > 0:
                net_income = fin.net_income
            else:
                net_income = self.loader.get_net_income(ticker)
            
            if net_income > 0:
                net_income_count += 1
            
            # --- Расчёт P/B ---
            pb = None
            if total_equity > 0 and shares > 0 and price > 0:
                book_value_per_share = total_equity / shares
                pb = price / book_value_per_share
            
            # --- Расчёт P/E ---
            pe = None
            if net_income > 0 and shares > 0 and price > 0:
                eps = net_income / shares
                if eps > 0:
                    pe = price / eps
            
            # --- Сохраняем результат ---
            result.append({
                'ticker': ticker,
                'name': sec['name'],
                'price': price,
                'market_cap': price * shares if price > 0 and shares > 0 else 0,
                'volume': price_info.get('volume', 0),
                'financials': fin,
                'pe': pe,
                'pb': pb,
                'shares_outstanding': shares,
            })
        
        # ==========================================
        # 5. ДИАГНОСТИКА
        # ==========================================
        print(f"📊 Загружено net_income для {net_income_count} компаний")
        
        self.companies = result
        logger.info(f"Обновлены данные для {len(result)} акций")
        return {
            'status': 'success',
            'total_companies': len(result),
            'companies': result,
        }
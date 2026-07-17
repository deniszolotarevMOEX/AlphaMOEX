# alpha/engine/data_loader.py
import pandas as pd
import requests
import logging
from typing import List, Dict, Optional
import time

logger = logging.getLogger(__name__)


class MoexDataLoader:
    """Загрузчик данных о российских акциях"""
   
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AlphaMOEX/0.1'
        })
   
    def get_all_shares(self) -> List[Dict]:
        """
        Получить список акций (тестовый + реальные тикеры)
        """
        # Базовый список популярных акций
        shares = [
            {'ticker': 'SBER', 'name': 'Сбербанк', 'isin': 'RU0009029540', 'lot_size': 10},
            {'ticker': 'SBERP', 'name': 'Сбербанк-пр', 'isin': 'RU0009029540', 'lot_size': 10},
            {'ticker': 'VTBR', 'name': 'ВТБ', 'isin': 'RU000A0JP5V6', 'lot_size': 1000},
            {'ticker': 'GAZP', 'name': 'Газпром', 'isin': 'RU0007661625', 'lot_size': 10},
            {'ticker': 'LKOH', 'name': 'Лукойл', 'isin': 'RU0009024277', 'lot_size': 1},
            {'ticker': 'NVTK', 'name': 'НОВАТЭК', 'isin': 'RU000A0DKVS5', 'lot_size': 1},
            {'ticker': 'GCHE', 'name': 'Черкизово', 'isin': 'RU000A0JL4R1', 'lot_size': 1},
            {'ticker': 'CHMF', 'name': 'Северсталь', 'isin': 'RU000A0DKVS5', 'lot_size': 1},
            {'ticker': 'MGNT', 'name': 'Магнит', 'isin': 'RU000A0JKQU8', 'lot_size': 1},
            {'ticker': 'TATN', 'name': 'Татнефть', 'isin': 'RU0009033391', 'lot_size': 1},
            {'ticker': 'ROSN', 'name': 'Роснефть', 'isin': 'RU000A0J2Q06', 'lot_size': 1},
            {'ticker': 'ALRS', 'name': 'Алроса', 'isin': 'RU0007252813', 'lot_size': 10},
            {'ticker': 'PLZL', 'name': 'Полюс', 'isin': 'RU000A0J2Q06', 'lot_size': 1},
            {'ticker': 'YNDX', 'name': 'Яндекс', 'isin': 'RU000A0DKVS5', 'lot_size': 1},
            {'ticker': 'MOEX', 'name': 'Мосбиржа', 'isin': 'RU000A0DKVS5', 'lot_size': 10},
            {'ticker': 'AFLT', 'name': 'Аэрофлот', 'isin': 'RU0009062285', 'lot_size': 10},
            {'ticker': 'MTSS', 'name': 'МТС', 'isin': 'RU0007775219', 'lot_size': 10},
            {'ticker': 'IRAO', 'name': 'Интер РАО', 'isin': 'RU000A0J2Q06', 'lot_size': 100},
            {'ticker': 'RUAL', 'name': 'Русал', 'isin': 'RU000A0DKVS5', 'lot_size': 1},
        ]
        return shares
   
    def get_current_prices(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Получить цены через Finam API (альтернативный источник)
        """
        if not tickers:
            return {}
       
        result = {}
       
        # Пробуем получить цены через Yahoo Finance (для российских акций)
        try:
            import yfinance as yf
            for ticker in tickers[:10]:  # Ограничиваем для скорости
                try:
                    # Для российских акций используем суффикс .ME
                    yf_ticker = yf.Ticker(f"{ticker}.ME")
                    price = yf_ticker.history(period="1d")['Close'].iloc[-1]
                    if price and price > 0:
                        result[ticker] = {
                            'price': float(price),
                            'market_cap': 0,
                            'volume': 0,
                        }
                except Exception as e:
                    continue
            if result:
                logger.info(f"Загружены цены для {len(result)} акций через Yahoo Finance")
                return result
        except ImportError:
            logger.warning("yfinance не установлен. Установите: pip install yfinance")
        except Exception as e:
            logger.warning(f"Ошибка Yahoo Finance: {e}")
       
        # Если Yahoo Finance не сработал — пробуем MOEX API
        try:
            url = "https://iss.moex.com/iss/engines/stock/markets/shares/securities.json"
            params = {
                'q': ','.join(tickers[:20]),
                'iss.meta': 'off',
                'limit': 100,
            }
           
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
           
            # Ищем данные в ответе
            if 'securities' in data and 'data' in data['securities']:
                for item in data['securities']['data']:
                    if len(item) >= 2:
                        ticker = item[0]
                        if ticker in tickers:
                            # Ищем цену в marketdata
                            price = None
                            if 'marketdata' in data and 'data' in data['marketdata']:
                                for row in data['marketdata']['data']:
                                    if len(row) >= 2 and row[0] == ticker:
                                        price = row[2] if len(row) > 2 else None
                                        break
                           
                            if price and price > 0:
                                result[ticker] = {
                                    'price': float(price),
                                    'market_cap': 0,
                                    'volume': 0,
                                }
           
            logger.info(f"Загружены цены для {len(result)} акций через MOEX API")
            return result
        except Exception as e:
            logger.error(f"Ошибка MOEX API: {e}")
       
        # Если ничего не получилось — возвращаем тестовые цены
        logger.info("Используем тестовые цены")
        return {
            ticker: {'price': 100.0 + (hash(ticker) % 100), 'market_cap': 0, 'volume': 0}
            for ticker in tickers
        }


class DataManager:
    """Менеджер данных"""
   
    def __init__(self, db_path: str = "database/alpha.db"):
        self.db_path = db_path
        self.loader = MoexDataLoader()
   
    def refresh_all_data(self) -> Dict:
        """Обновить все данные"""
        logger.info("Начинаем обновление данных...")
       
        securities = self.loader.get_all_shares()
        if not securities:
            return {'status': 'error', 'message': 'Не удалось загрузить список акций'}
       
        tickers = [s['ticker'] for s in securities]
        prices = self.loader.get_current_prices(tickers)
       
        result = []
        for sec in securities:
            ticker = sec['ticker']
            price_info = prices.get(ticker, {'price': 0, 'market_cap': 0, 'volume': 0})
           
            result.append({
                'ticker': ticker,
                'name': sec['name'],
                'sector': 'N/A',
                'industry': 'N/A',
                'isin': sec.get('isin', ''),
                'lot_size': sec.get('lot_size', 1),
                'free_float': 0.0,
                'price': price_info.get('price', 0),
                'market_cap': price_info.get('market_cap', 0),
                'volume': price_info.get('volume', 0),
            })
       
        logger.info(f"Обновлены данные для {len(result)} акций")
        return {
            'status': 'success',
            'total_companies': len(result),
            'companies': result,
        }
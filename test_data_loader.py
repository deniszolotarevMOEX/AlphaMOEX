# test_data_loader.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from alpha.engine.data_loader import MoexDataLoader, DataManager

def test_moex_loader():
    """Тестируем загрузку данных"""
    print("=" * 50)
    print("Тестирование загрузчика данных Alpha MOEX")
    print("=" * 50)
   
    loader = MoexDataLoader()
   
    # 1. Загружаем список акций
    print("\n1. Загрузка списка акций...")
    shares = loader.get_all_shares()
    print(f"   Загружено: {len(shares)} акций")
    if shares:
        print(f"   Пример: {shares[0]['ticker']} — {shares[0]['name']}")
   
    # 2. Загружаем цены
    if shares:
        tickers = [s['ticker'] for s in shares[:5]]
        print(f"\n2. Загрузка цен для {len(tickers)} акций...")
        prices = loader.get_current_prices(tickers)
        for ticker, info in prices.items():
            print(f"   {ticker}: {info.get('price', 'Н/Д')} руб.")
   
    # 3. Полное обновление
    print("\n3. Полное обновление данных...")
    manager = DataManager()
    result = manager.refresh_all_data()
   
    if result['status'] == 'success':
        print(f"   Успешно! Обработано: {result['total_companies']} компаний")
        if result['companies']:
            first = result['companies'][0]
            print(f"   Пример: {first['ticker']} — {first['name']} — {first['price']} руб.")
    else:
        print(f"   Ошибка: {result.get('message', 'Неизвестная ошибка')}")
   
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_moex_loader()
# alpha/ui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QHeaderView, QLabel,
    QSplitter, QTextEdit, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt

from ..engine.scoring.scorer import AlphaScorer
from ..engine.scoring.data import (
    VSYDP_COMPANY, VSYDP_FINANCIALS, VSYDP_MULTIPLIERS,
    GCHE_COMPANY, GCHE_FINANCIALS, GCHE_MULTIPLIERS,
    NVTK_COMPANY, NVTK_FINANCIALS, NVTK_MULTIPLIERS,
    CHMF_COMPANY, CHMF_FINANCIALS, CHMF_MULTIPLIERS,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
       
        self.setWindowTitle("Alpha MOEX")
        self.setGeometry(100, 100, 1200, 700)
       
        # Создаём скоринг-модель
        self.scorer = AlphaScorer()
       
        # Данные для таблицы (тестовые)
        self.companies = [
            {
                'ticker': 'VSYDP',
                'company': VSYDP_COMPANY,
                'financials': VSYDP_FINANCIALS,
                'multipliers': VSYDP_MULTIPLIERS,
            },
            {
                'ticker': 'GCHE',
                'company': GCHE_COMPANY,
                'financials': GCHE_FINANCIALS,
                'multipliers': GCHE_MULTIPLIERS,
            },
            {
                'ticker': 'NVTK',
                'company': NVTK_COMPANY,
                'financials': NVTK_FINANCIALS,
                'multipliers': NVTK_MULTIPLIERS,
            },
            {
                'ticker': 'CHMF',
                'company': CHMF_COMPANY,
                'financials': CHMF_FINANCIALS,
                'multipliers': CHMF_MULTIPLIERS,
            },
        ]
       
        # Рассчитываем рейтинги
        self.results = []
        for item in self.companies:
            result = self.scorer.score_company(
                company=item['company'],
                financials=item['financials'],
                multipliers=item['multipliers']
            )
            self.results.append({
                'ticker': item['ticker'],
                'name': item['company'].name,
                'result': result
            })
       
        # Создаём интерфейс
        self._setup_ui()
        print(f"🟢 Инициализация завершена. Компаний: {len(self.companies)}, Результатов: {len(self.results)}")
   
    def _setup_ui(self):
        """Создаёт виджеты интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный горизонтальный сплиттер
        main_splitter = QSplitter(Qt.Horizontal)
       
        # Левая панель — таблица акций
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Тикер", "Компания", "Цена", "P/E", "P/B", "Рейтинг", "Оценка", "Решение"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSortingEnabled(True)  # <-- СОРТИРОВКА ВКЛЮЧЕНА
        self.table.itemSelectionChanged.connect(self._on_select_company)
        
        self._populate_table()
       
        # Правая панель — карточка компании
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
       
        self.company_title = QLabel("Выберите акцию")
        self.company_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        right_layout.addWidget(self.company_title)
       
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        right_layout.addWidget(self.details_text)
       
        # Кнопка "Обновить"
        btn_layout = QHBoxLayout()
        btn_refresh = QPushButton("🔄 Обновить")
        btn_refresh.clicked.connect(self._refresh)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_refresh)
        right_layout.addLayout(btn_layout)
       
        # Добавляем панели в сплиттер
        main_splitter.addWidget(self.table)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([700, 500])
       
        layout = QVBoxLayout(central_widget)
        layout.addWidget(main_splitter)
   
    def _populate_table(self):
        """Заполняет таблицу данными"""
        self.table.setRowCount(len(self.results))
        
        for i, item in enumerate(self.results):
            result = item['result']
            ticker = item['ticker']
            name = item['name']
            total = result['total']
            grade = result['grade']
            
            # Находим цену, P/E и P/B
            price = 0.0
            pe = None
            pb = None
            for comp in self.companies:
                if comp['ticker'] == ticker:
                    price = comp['multipliers'].price
                    pe = comp['multipliers'].pe
                    pb = comp['multipliers'].pb
                    break
            
            # Решение
            if total >= 900:
                solution = "🟢 Покупать"
            elif total >= 800:
                solution = "🟡 Малой долей"
            elif total >= 700:
                solution = "🟠 Наблюдать"
            else:
                solution = "🔴 Избегать"
            
            # Форматируем P/E и P/B
            pe_text = f"{pe:.2f}" if pe is not None else "—"
            pb_text = f"{pb:.2f}" if pb is not None else "—"
            
            self.table.setItem(i, 0, QTableWidgetItem(ticker))
            self.table.setItem(i, 1, QTableWidgetItem(name))
            self.table.setItem(i, 2, QTableWidgetItem(f"{price:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(pe_text))
            self.table.setItem(i, 4, QTableWidgetItem(pb_text))
            self.table.setItem(i, 5, QTableWidgetItem(str(total)))
            self.table.setItem(i, 6, QTableWidgetItem(grade))
            self.table.setItem(i, 7, QTableWidgetItem(solution))
   
    def _on_select_company(self):
        """При выборе строки показывает карточку компании"""
        selected = self.table.selectedItems()
        if not selected:
            return
       
        row = selected[0].row()
        item = self.results[row]
        result = item['result']
       
        self.company_title.setText(f"{item['ticker']} — {item['name']}")
       
        details = f"""
Рейтинг: {result['total']} / 1000  |  Оценка: {result['grade']}

📈 Детализация:
  • Качество бизнеса:       {result['quality']} / 200
  • Фин. устойчивость:      {result['stability']} / 150
  • Недооценённость:        {result['undervaluation']} / 250
  • Рост бизнеса:           {result['growth']} / 100
  • Денежный поток:         {result['cash_flow']} / 100
  • Капитал и акционеры:    {result['equity']} / 50
  • Рын. неэффективность:   {result['inefficiency']} / 100
  • Катализаторы:           {result['catalysts']} / 50

💡 Рекомендация:
  • Покупать, если рейтинг ≥ 900
  • Малой долей, если ≥ 800
  • Наблюдать, если ≥ 700
  • Избегать, если < 700
        """
        self.details_text.setText(details)
   
    def _refresh(self):
        """Обновляет данные с диагностикой"""
        self.details_text.setText("🔄 Загрузка данных...")
        
        from ..engine.data_loader import DataManager
        manager = DataManager()
        data_result = manager.refresh_all_data()
        
        if data_result['status'] != 'success':
            self.details_text.setText(f"❌ Ошибка: {data_result.get('message')}")
            return
        
        loaded_companies = data_result['companies']
        # ⬇️ ДИАГНОСТИКА: печатаем первые 3 компании с P/E и P/B
        print("\n" + "="*60)
        print("🐞 ДИАГНОСТИКА: P/E и P/B из data_loader")
        print("="*60)
        for i, item in enumerate(loaded_companies[:3]):
            print(f"[{i+1}] {item['ticker']} — P/E: {item.get('pe')}, P/B: {item.get('pb')}")
        print("="*60 + "\n")
        if not loaded_companies:
            self.details_text.setText("⚠️ Данные не загружены")
            return
        
        # Перестраиваем self.companies
        new_companies = []
        for item in loaded_companies:
            ticker = item['ticker']
            old_item = next((c for c in self.companies if c['ticker'] == ticker), None)
            
            if old_item:
                company = old_item['company']
                financials = item.get('financials') or old_item['financials']
                multipliers = old_item['multipliers']
                multipliers.price = item['price']
                # ⬇️ КРИТИЧЕСКИ ВАЖНО: обновляем P/E и P/B
                multipliers.pe = item.get('pe')
                multipliers.pb = item.get('pb')
                
                new_companies.append({
                    'ticker': ticker,
                    'company': company,
                    'financials': financials,
                    'multipliers': multipliers,
                })
            else:
                from ..engine.scoring.models import Company, Financials, Multipliers
                company = Company(ticker=ticker, name=item['name'], sector='N/A')
                financials = item.get('financials') or Financials(ticker=ticker)
                multipliers = Multipliers(
                    ticker=ticker,
                    price=item['price'],
                    pe=item.get('pe'),
                    pb=item.get('pb'),
                )
                new_companies.append({
                    'ticker': ticker,
                    'company': company,
                    'financials': financials,
                    'multipliers': multipliers,
                })
        
        self.companies = new_companies
        
                # ⬇️ ДИАГНОСТИКА: проверяем, что в self.companies есть P/E и P/B
        print("\n" + "="*60)
        print("🐞 ДИАГНОСТИКА: self.companies после обновления")
        print("="*60)
        for i, comp in enumerate(self.companies[:3]):
            print(f"[{i+1}] {comp['ticker']} — P/E: {comp['multipliers'].pe}, P/B: {comp['multipliers'].pb}")
        print("="*60 + "\n")
        
        # Пересчитываем рейтинги
        self.results = []
        for item in self.companies:
            result = self.scorer.score_company(
                company=item['company'],
                financials=item['financials'],
                multipliers=item['multipliers']
            )
            self.results.append({
                'ticker': item['ticker'],
                'name': item['company'].name,
                'result': result
            })
        
        self._populate_table()
        self.details_text.setText(f"✅ Данные обновлены! ({len(self.companies)} компаний)")
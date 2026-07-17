# test_integration.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from alpha.ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
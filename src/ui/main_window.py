from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, 
    QHBoxLayout, QLabel, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from .sondeur_view import SondeurView
from .essai_view import EssaiView
from .chantier_view import ChantierView
from .affectation_view import AffectationView
from .carbon_footprint_view import CarbonFootprintView


class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setup_ui()
        self.setup_styling()

    def setup_ui(self):
        self.setWindowTitle("Planificateur de Tâches — Sondeurs")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Navigation sidebar
        nav_widget = self.create_navigation()
        main_layout.addWidget(nav_widget, 0)
        
        # Tab widget for main content
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        
        # Create tabs
        self.sondeur_view = SondeurView(self.session)
        self.essai_view = EssaiView(self.session)
        self.chantier_view = ChantierView(self.session)
        self.affectation_view = AffectationView(self.session)
        self.carbon_footprint_view = CarbonFootprintView(self.session)
        
        self.tab_widget.addTab(self.sondeur_view, "👤 Sondeurs")
        self.tab_widget.addTab(self.essai_view, "🔬 Essais")
        self.tab_widget.addTab(self.chantier_view, "🏗️ Chantiers")
        self.tab_widget.addTab(self.affectation_view, "📋 Affectations")
        self.tab_widget.addTab(self.carbon_footprint_view, "🌱 Empreinte Carbone")
        
        main_layout.addWidget(self.tab_widget, 1)

    def create_navigation(self):
        nav_widget = QWidget()
        nav_widget.setFixedWidth(200)
        nav_layout = QVBoxLayout(nav_widget)
        
        # Title
        title_label = QLabel("Services")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title_label.setFont(title_font)
        nav_layout.addWidget(title_label)
        
        nav_layout.addSpacing(20)
        
        # Navigation buttons
        buttons = [
            ("👤 Sondeurs", 0),
            ("🔬 Essais", 1),
            ("🏗️ Chantiers", 2),
            ("📋 Affectations", 3),
            ("🌱 Empreinte Carbone", 4)
        ]
        
        for text, tab_index in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(40)
            btn.clicked.connect(lambda checked, idx=tab_index: self.tab_widget.setCurrentIndex(idx))
            nav_layout.addWidget(btn)
        
        nav_layout.addStretch()
        return nav_widget

    def setup_styling(self):
        """Apply modern styling to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            
            QTabWidget::tab-bar {
                alignment: left;
            }
            
            QTabBar::tab {
                background: #e1e1e1;
                border: 1px solid #c0c0c0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
            
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                alternate-background-color: #f9f9f9;
            }
            
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
        """)

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QSpinBox, QDateEdit, QComboBox,
    QPushButton, QLabel, QDialogButtonBox, QMessageBox, QCheckBox
)
from PyQt5.QtCore import QDate, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from src.models import Sondeur, Essai, Chantier, UniteTravail
from src.carbon_footprint import CarbonFootprintCalculator
from datetime import date


class CarbonFootprintThread(QThread):
    """Thread for calculating carbon footprint without blocking UI"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, sondeur_address, chantier_address, days):
        super().__init__()
        self.sondeur_address = sondeur_address
        self.chantier_address = chantier_address
        self.days = days
        self.calculator = CarbonFootprintCalculator()
    
    def run(self):
        try:
            result = self.calculator.calculate_affectation_footprint(
                self.sondeur_address, 
                self.chantier_address, 
                self.days
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class BaseFormDialog(QDialog):
    """Base class for form dialogs with common styling"""
    
    def __init__(self, parent=None, title="Formulaire"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setup_styling()
    
    def setup_styling(self):
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
            QLineEdit, QTextEdit, QSpinBox, QDateEdit, QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDateEdit:focus, QComboBox:focus {
                border-color: #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton[text="Annuler"] {
                background-color: #f44336;
            }
            QPushButton[text="Annuler"]:hover {
                background-color: #da190b;
            }
        """)


class SondeurForm(BaseFormDialog):
    def __init__(self, parent=None, sondeur=None):
        super().__init__(parent, "Nouveau Sondeur" if sondeur is None else "Modifier Sondeur")
        self.sondeur = sondeur
        self.setup_form()
    
    def setup_form(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Informations du Sondeur")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Nom complet du sondeur")
        form_layout.addRow("Nom *:", self.name_edit)
        
        self.address_edit = QTextEdit()
        self.address_edit.setPlaceholderText("Adresse complète (optionnel)")
        self.address_edit.setMaximumHeight(80)
        form_layout.addRow("Adresse:", self.address_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Enregistrer")
        self.cancel_button = QPushButton("Annuler")
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        # Fill form if editing
        if self.sondeur:
            self.name_edit.setText(self.sondeur.name)
            self.address_edit.setPlainText(self.sondeur.address or "")
    
    def get_data(self):
        return {
            'name': self.name_edit.text().strip(),
            'address': self.address_edit.toPlainText().strip() or None
        }
    
    def accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire!")
            return
        super().accept()


class EssaiForm(BaseFormDialog):
    def __init__(self, parent=None, essai=None):
        super().__init__(parent, "Nouvel Essai" if essai is None else "Modifier Essai")
        self.essai = essai
        self.setup_form()
    
    def setup_form(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Informations de l'Essai")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Nom de l'essai")
        form_layout.addRow("Nom *:", self.name_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Description détaillée de l'essai (optionnel)")
        self.description_edit.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Enregistrer")
        self.cancel_button = QPushButton("Annuler")
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        # Fill form if editing
        if self.essai:
            self.name_edit.setText(self.essai.name)
            self.description_edit.setPlainText(self.essai.description or "")
    
    def get_data(self):
        return {
            'name': self.name_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip() or None
        }
    
    def accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire!")
            return
        super().accept()


class ChantierForm(BaseFormDialog):
    def __init__(self, parent=None, chantier=None):
        super().__init__(parent, "Nouveau Chantier" if chantier is None else "Modifier Chantier")
        self.chantier = chantier
        self.setup_form()
    
    def setup_form(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Informations du Chantier")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Nom du chantier")
        form_layout.addRow("Nom *:", self.name_edit)
        
        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("Lieu du chantier")
        form_layout.addRow("Lieu:", self.location_edit)
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow("Date de début:", self.date_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Enregistrer")
        self.cancel_button = QPushButton("Annuler")
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        # Fill form if editing
        if self.chantier:
            self.name_edit.setText(self.chantier.name)
            self.location_edit.setText(self.chantier.location or "")
            if self.chantier.date:
                self.date_edit.setDate(QDate.fromString(self.chantier.date.isoformat(), "yyyy-MM-dd"))
    
    def get_data(self):
        return {
            'name': self.name_edit.text().strip(),
            'location': self.location_edit.text().strip() or None,
            'date': self.date_edit.date().toPyDate()
        }
    
    def accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire!")
            return
        super().accept()


class AffectationForm(BaseFormDialog):
    def __init__(self, parent=None, session=None, unite_travail=None):
        super().__init__(parent, "Nouvelle Affectation" if unite_travail is None else "Modifier Affectation")
        self.session = session
        self.unite_travail = unite_travail
        self.setup_form()
    
    def setup_form(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Affectation d'Unité de Travail")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Chantier combo
        self.chantier_combo = QComboBox()
        chantiers = self.session.query(Chantier).order_by(Chantier.name).all()
        for chantier in chantiers:
            self.chantier_combo.addItem(f"{chantier.name} ({chantier.location or 'Lieu non spécifié'})", chantier.id)
        form_layout.addRow("Chantier *:", self.chantier_combo)
        
        # Essai combo
        self.essai_combo = QComboBox()
        essais = self.session.query(Essai).order_by(Essai.name).all()
        for essai in essais:
            self.essai_combo.addItem(f"{essai.name} - {essai.description or 'Pas de description'}", essai.id)
        form_layout.addRow("Essai *:", self.essai_combo)
        
        # Sondeur combo
        self.sondeur_combo = QComboBox()
        sondeurs = self.session.query(Sondeur).order_by(Sondeur.name).all()
        for sondeur in sondeurs:
            self.sondeur_combo.addItem(f"{sondeur.name} ({sondeur.address or 'Pas d\'adresse'})", sondeur.id)
        form_layout.addRow("Sondeur *:", self.sondeur_combo)
        
        # Days spinbox
        self.days_spin = QSpinBox()
        self.days_spin.setMinimum(1)
        self.days_spin.setMaximum(365)
        self.days_spin.setValue(1)
        self.days_spin.setSuffix(" jour(s)")
        form_layout.addRow("Durée *:", self.days_spin)
        
        # Date edit
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow("Date de début:", self.date_edit)
        
        # Carbon footprint checkbox
        self.calc_carbon_checkbox = QCheckBox("Calculer l'empreinte carbone automatiquement")
        self.calc_carbon_checkbox.setChecked(True)
        form_layout.addRow("", self.calc_carbon_checkbox)
        
        # Carbon footprint display
        self.carbon_info_label = QLabel("Empreinte carbone: Non calculée")
        self.carbon_info_label.setStyleSheet("color: #666; font-style: italic; padding: 5px;")
        form_layout.addRow("", self.carbon_info_label)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Enregistrer")
        self.cancel_button = QPushButton("Annuler")
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        # Connect form changes to carbon footprint calculation
        self.sondeur_combo.currentTextChanged.connect(self.calculate_carbon_footprint)
        self.chantier_combo.currentTextChanged.connect(self.calculate_carbon_footprint)
        self.days_spin.valueChanged.connect(self.calculate_carbon_footprint)
        self.calc_carbon_checkbox.toggled.connect(self.calculate_carbon_footprint)
        
        # Initialize calculated values
        self.calculated_distance = None
        self.calculated_co2 = None
        
        # Fill form if editing
        if self.unite_travail:
            # Set combo selections based on existing data
            for i in range(self.chantier_combo.count()):
                if self.chantier_combo.itemData(i) == self.unite_travail.chantier_id:
                    self.chantier_combo.setCurrentIndex(i)
                    break
            
            for i in range(self.essai_combo.count()):
                if self.essai_combo.itemData(i) == self.unite_travail.essai_id:
                    self.essai_combo.setCurrentIndex(i)
                    break
            
            for i in range(self.sondeur_combo.count()):
                if self.sondeur_combo.itemData(i) == self.unite_travail.sondeur_id:
                    self.sondeur_combo.setCurrentIndex(i)
                    break
            
            self.days_spin.setValue(self.unite_travail.days)
            if self.unite_travail.date_debut:
                self.date_edit.setDate(QDate.fromString(self.unite_travail.date_debut.isoformat(), "yyyy-MM-dd"))
    
    def get_data(self):
        return {
            'chantier_id': self.chantier_combo.currentData(),
            'essai_id': self.essai_combo.currentData(),
            'sondeur_id': self.sondeur_combo.currentData(),
            'days': self.days_spin.value(),
            'date_debut': self.date_edit.date().toPyDate(),
            'calculate_carbon': self.calc_carbon_checkbox.isChecked()
        }
    
    def calculate_carbon_footprint(self):
        """Calculate carbon footprint for the current form data"""
        if not self.calc_carbon_checkbox.isChecked():
            return
        
        # Get addresses
        sondeur_id = self.sondeur_combo.currentData()
        chantier_id = self.chantier_combo.currentData()
        
        if not sondeur_id or not chantier_id:
            return
        
        sondeur = self.session.query(Sondeur).get(sondeur_id)
        chantier = self.session.query(Chantier).get(chantier_id)
        
        if not sondeur or not chantier or not sondeur.address or not chantier.location:
            self.carbon_info_label.setText("Empreinte carbone: Adresses manquantes")
            self.carbon_info_label.setStyleSheet("color: #ff6b6b; font-style: italic; padding: 5px;")
            return
        
        # Start calculation
        self.carbon_info_label.setText("Empreinte carbone: Calcul en cours...")
        self.carbon_info_label.setStyleSheet("color: #666; font-style: italic; padding: 5px;")
        
        self.carbon_thread = CarbonFootprintThread(
            sondeur.address,
            chantier.location,
            self.days_spin.value()
        )
        self.carbon_thread.finished.connect(self.on_carbon_calculated)
        self.carbon_thread.error.connect(self.on_carbon_error)
        self.carbon_thread.start()
    
    def on_carbon_calculated(self, result):
        """Handle carbon footprint calculation result"""
        if result['error']:
            self.carbon_info_label.setText(f"Empreinte carbone: {result['error']}")
            self.carbon_info_label.setStyleSheet("color: #ff6b6b; font-style: italic; padding: 5px;")
        else:
            distance = result['distance_km']
            co2 = result['co2_kg']
            self.carbon_info_label.setText(f"Empreinte carbone: {distance:.2f} km, {co2:.2f} kg CO₂")
            self.carbon_info_label.setStyleSheet("color: #28a745; font-style: italic; padding: 5px;")
            
            # Store the calculated values for later use
            self.calculated_distance = distance
            self.calculated_co2 = co2
    
    def on_carbon_error(self, error):
        """Handle carbon footprint calculation error"""
        self.carbon_info_label.setText(f"Erreur calcul: {error}")
        self.carbon_info_label.setStyleSheet("color: #ff6b6b; font-style: italic; padding: 5px;")
    
    def accept(self):
        if not self.chantier_combo.currentData():
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un chantier!")
            return
        if not self.essai_combo.currentData():
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un essai!")
            return
        if not self.sondeur_combo.currentData():
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un sondeur!")
            return
        super().accept()

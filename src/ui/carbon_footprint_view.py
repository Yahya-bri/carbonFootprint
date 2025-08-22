from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QTableWidget, QTableWidgetItem, QGroupBox,
    QMessageBox, QProgressDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from src.carbon_footprint import CarbonFootprintCalculator


class CarbonFootprintCalculationThread(QThread):
    """Thread for calculating carbon footprint to avoid blocking UI"""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.calculator = CarbonFootprintCalculator()
    
    def run(self):
        try:
            summary = self.calculator.get_summary_by_sondeur(self.session)
            self.finished.emit(summary)
        except Exception as e:
            self.error.emit(str(e))


class CarbonFootprintView(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.calculator = CarbonFootprintCalculator()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("🌱 Empreinte Carbone")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Calculate button
        self.calc_button = QPushButton("🔄 Calculer l'Empreinte Carbone")
        self.calc_button.setFixedHeight(40)
        self.calc_button.clicked.connect(self.calculate_footprint)
        header_layout.addWidget(self.calc_button)
        
        layout.addLayout(header_layout)
        
        # Summary group
        summary_group = QGroupBox("📊 Résumé Général")
        summary_layout = QVBoxLayout(summary_group)
        
        self.total_distance_label = QLabel("Distance totale: - km")
        self.total_co2_label = QLabel("Émissions CO₂ totales: - kg")
        self.total_affectations_label = QLabel("Affectations avec calcul: -")
        
        for label in [self.total_distance_label, self.total_co2_label, self.total_affectations_label]:
            label.setStyleSheet("font-size: 14px; padding: 5px;")
            summary_layout.addWidget(label)
        
        layout.addWidget(summary_group)
        
        # Per sondeur group
        sondeur_group = QGroupBox("👤 Détail par Sondeur")
        sondeur_layout = QVBoxLayout(sondeur_group)
        
        # Table for sondeur details
        self.sondeur_table = QTableWidget()
        self.sondeur_table.setColumnCount(4)
        self.sondeur_table.setHorizontalHeaderLabels([
            "Sondeur", "Distance (km)", "CO₂ (kg)", "Affectations"
        ])
        self.sondeur_table.horizontalHeader().setStretchLastSection(True)
        
        sondeur_layout.addWidget(self.sondeur_table)
        layout.addWidget(sondeur_group)
        
        # Information label
        info_label = QLabel("""
        <b>Informations sur le calcul :</b><br>
        • Distance = distance de trajet × 2 (aller-retour) × nombre de jours<br>
        • CO₂ = distance × 0.120 kg/km (véhicule moyen)<br>
        • Seules les affectations avec adresses valides sont incluses
        """)
        info_label.setStyleSheet("color: #666; font-size: 11px; padding: 10px; background-color: #f9f9f9; border-radius: 5px;")
        layout.addWidget(info_label)
        
        # Initial calculation
        self.calculate_footprint()
    
    def calculate_footprint(self):
        """Calculate carbon footprint for all affectations"""
        self.calc_button.setEnabled(False)
        self.calc_button.setText("🔄 Calcul en cours...")
        
        # Create progress dialog
        progress = QProgressDialog("Calcul de l'empreinte carbone...", "Annuler", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        
        # Start calculation thread
        self.calc_thread = CarbonFootprintCalculationThread(self.session)
        self.calc_thread.finished.connect(lambda summary: self.on_calculation_finished(summary, progress))
        self.calc_thread.error.connect(lambda error: self.on_calculation_error(error, progress))
        self.calc_thread.start()
    
    def on_calculation_finished(self, summary, progress):
        """Handle calculation completion"""
        progress.close()
        
        # Update summary
        totals = summary['totals']
        self.total_distance_label.setText(f"Distance totale: {totals['total_distance_km']:.2f} km")
        self.total_co2_label.setText(f"Émissions CO₂ totales: {totals['total_co2_kg']:.2f} kg")
        self.total_affectations_label.setText(f"Affectations avec calcul: {totals['total_affectations']}")
        
        # Update table
        by_sondeur = summary['by_sondeur']
        self.sondeur_table.setRowCount(len(by_sondeur))
        
        for row, (sondeur_name, data) in enumerate(by_sondeur.items()):
            self.sondeur_table.setItem(row, 0, QTableWidgetItem(sondeur_name))
            self.sondeur_table.setItem(row, 1, QTableWidgetItem(f"{data['total_distance_km']:.2f}"))
            self.sondeur_table.setItem(row, 2, QTableWidgetItem(f"{data['total_co2_kg']:.2f}"))
            self.sondeur_table.setItem(row, 3, QTableWidgetItem(str(data['affectations_count'])))
        
        # Reset button
        self.calc_button.setEnabled(True)
        self.calc_button.setText("🔄 Calculer l'Empreinte Carbone")
        
        # Show completion message
        if totals['total_affectations'] > 0:
            QMessageBox.information(
                self, 
                "Calcul terminé", 
                f"Empreinte carbone calculée pour {totals['total_affectations']} affectations.\n"
                f"Total: {totals['total_distance_km']:.2f} km, {totals['total_co2_kg']:.2f} kg CO₂"
            )
        else:
            QMessageBox.information(
                self, 
                "Aucune donnée", 
                "Aucune affectation avec distances calculées trouvée.\n"
                "Assurez-vous d'avoir des affectations avec des adresses valides."
            )
    
    def on_calculation_error(self, error, progress):
        """Handle calculation error"""
        progress.close()
        
        self.calc_button.setEnabled(True)
        self.calc_button.setText("🔄 Calculer l'Empreinte Carbone")
        
        QMessageBox.critical(
            self, 
            "Erreur de calcul", 
            f"Erreur lors du calcul de l'empreinte carbone:\n{error}"
        )

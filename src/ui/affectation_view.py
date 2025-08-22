from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QLabel, QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.models import UniteTravail, Sondeur, Essai, Chantier
from .forms import AffectationForm


class AffectationView(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setup_ui()
        self.refresh_list()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Gestion des Affectations")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Action buttons
        self.add_button = QPushButton("➕ Nouvelle Affectation")
        self.edit_button = QPushButton("✏️ Modifier")
        self.delete_button = QPushButton("🗑️ Supprimer")
        
        self.add_button.clicked.connect(self.add_affectation)
        self.edit_button.clicked.connect(self.edit_affectation)
        self.delete_button.clicked.connect(self.delete_affectation)
        
        header_layout.addWidget(self.add_button)
        header_layout.addWidget(self.edit_button)
        header_layout.addWidget(self.delete_button)
        
        layout.addLayout(header_layout)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.list_widget)
        
        # Initially disable edit/delete buttons
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
    
    def refresh_list(self):
        self.list_widget.clear()
        unites = self.session.query(UniteTravail).order_by(UniteTravail.date_debut).all()
        
        for unite in unites:
            item = QListWidgetItem()
            
            # Get related objects
            chantier = unite.chantier
            essai = unite.essai
            sondeur = unite.sondeur
            
            # Main text
            main_text = f"🏗️ {chantier.name if chantier else 'Chantier inconnu'} • 🔬 {essai.name if essai else 'Essai inconnu'}"
            
            # Subtitle with sondeur, duration and date
            subtitle_parts = []
            if sondeur:
                subtitle_parts.append(f"👤 {sondeur.name}")
            subtitle_parts.append(f"⏱️ {unite.days} jour(s)")
            if unite.date_debut:
                subtitle_parts.append(f"📅 {unite.date_debut.strftime('%d/%m/%Y')}")
            
            item.setText(f"{main_text}\n{' • '.join(subtitle_parts)}")
            item.setData(Qt.UserRole, (unite.chantier_id, unite.essai_id))
            
            self.list_widget.addItem(item)
    
    def on_selection_changed(self):
        has_selection = bool(self.list_widget.selectedItems())
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
    
    def add_affectation(self):
        # Check if we have required data
        if not self.session.query(Chantier).first():
            QMessageBox.warning(self, "Erreur", "Aucun chantier disponible. Ajoutez d'abord des chantiers.")
            return
        if not self.session.query(Essai).first():
            QMessageBox.warning(self, "Erreur", "Aucun essai disponible. Ajoutez d'abord des essais.")
            return
        if not self.session.query(Sondeur).first():
            QMessageBox.warning(self, "Erreur", "Aucun sondeur disponible. Ajoutez d'abord des sondeurs.")
            return
        
        form = AffectationForm(self, self.session)
        if form.exec_() == form.Accepted:
            data = form.get_data()
            try:
                # Create the affectation
                unite_data = {k: v for k, v in data.items() if k != 'calculate_carbon'}
                unite = UniteTravail(**unite_data)
                
                # Add carbon footprint data if calculated
                if hasattr(form, 'calculated_distance') and form.calculated_distance is not None:
                    unite.distance_km = form.calculated_distance
                    unite.co2_kg = form.calculated_co2
                
                self.session.add(unite)
                self.session.commit()
                self.refresh_list()
                
                # Show success message with carbon footprint info
                message = "Affectation créée avec succès!"
                if unite.distance_km is not None:
                    message += f"\nEmpreinte carbone: {unite.distance_km:.2f} km, {unite.co2_kg:.2f} kg CO₂"
                QMessageBox.information(self, "Succès", message)
            except Exception as e:
                self.session.rollback()
                if "UNIQUE constraint failed" in str(e):
                    QMessageBox.warning(self, "Erreur", 
                        "Cette combinaison chantier-essai existe déjà.\n"
                        "Un même essai ne peut être affecté qu'une seule fois par chantier.")
                else:
                    QMessageBox.critical(self, "Erreur", f"Erreur lors de la création: {str(e)}")
    
    def edit_affectation(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            return
        
        chantier_id, essai_id = current_item.data(Qt.UserRole)
        unite = self.session.query(UniteTravail).filter_by(
            chantier_id=chantier_id, essai_id=essai_id
        ).first()
        
        if not unite:
            QMessageBox.warning(self, "Erreur", "Affectation non trouvée!")
            return
        
        form = AffectationForm(self, self.session, unite)
        if form.exec_() == form.Accepted:
            data = form.get_data()
            try:
                # Update the unite_travail
                unite.sondeur_id = data['sondeur_id']
                unite.days = data['days']
                unite.date_debut = data['date_debut']
                self.session.commit()
                self.refresh_list()
                QMessageBox.information(self, "Succès", "Affectation modifiée avec succès!")
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification: {str(e)}")
    
    def delete_affectation(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            return
        
        chantier_id, essai_id = current_item.data(Qt.UserRole)
        unite = self.session.query(UniteTravail).filter_by(
            chantier_id=chantier_id, essai_id=essai_id
        ).first()
        
        if not unite:
            QMessageBox.warning(self, "Erreur", "Affectation non trouvée!")
            return
        
        chantier_name = unite.chantier.name if unite.chantier else "Inconnu"
        essai_name = unite.essai.name if unite.essai else "Inconnu"
        
        reply = QMessageBox.question(
            self, "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer l'affectation ?\n\n"
            f"Chantier: {chantier_name}\n"
            f"Essai: {essai_name}\n\n"
            f"Cette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.session.delete(unite)
            self.session.commit()
            self.refresh_list()
            QMessageBox.information(self, "Succès", "Affectation supprimée avec succès!")

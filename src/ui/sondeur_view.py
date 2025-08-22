from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QLabel, QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.models import Sondeur
from .forms import SondeurForm


class SondeurView(QWidget):
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
        
        title = QLabel("Gestion des Sondeurs")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Action buttons
        self.add_button = QPushButton("➕ Nouveau Sondeur")
        self.edit_button = QPushButton("✏️ Modifier")
        self.delete_button = QPushButton("🗑️ Supprimer")
        
        self.add_button.clicked.connect(self.add_sondeur)
        self.edit_button.clicked.connect(self.edit_sondeur)
        self.delete_button.clicked.connect(self.delete_sondeur)
        
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
        sondeurs = self.session.query(Sondeur).order_by(Sondeur.name).all()
        
        for sondeur in sondeurs:
            item = QListWidgetItem()
            item.setText(f"{sondeur.name}")
            item.setData(Qt.UserRole, sondeur.id)
            
            # Add subtitle with address
            if sondeur.address:
                item.setText(f"{sondeur.name}\n📍 {sondeur.address}")
            
            self.list_widget.addItem(item)
    
    def on_selection_changed(self):
        has_selection = bool(self.list_widget.selectedItems())
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
    
    def add_sondeur(self):
        form = SondeurForm(self)
        if form.exec_() == form.Accepted:
            data = form.get_data()
            sondeur = Sondeur(**data)
            self.session.add(sondeur)
            self.session.commit()
            self.refresh_list()
            QMessageBox.information(self, "Succès", f"Sondeur '{data['name']}' ajouté avec succès!")
    
    def edit_sondeur(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            return
        
        sondeur_id = current_item.data(Qt.UserRole)
        sondeur = self.session.get(Sondeur, sondeur_id)
        
        form = SondeurForm(self, sondeur)
        if form.exec_() == form.Accepted:
            data = form.get_data()
            sondeur.name = data['name']
            sondeur.address = data['address']
            self.session.commit()
            self.refresh_list()
            QMessageBox.information(self, "Succès", "Sondeur modifié avec succès!")
    
    def delete_sondeur(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            return
        
        sondeur_id = current_item.data(Qt.UserRole)
        sondeur = self.session.get(Sondeur, sondeur_id)
        
        reply = QMessageBox.question(
            self, "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer le sondeur '{sondeur.name}' ?\n\nCette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.session.delete(sondeur)
            self.session.commit()
            self.refresh_list()
            QMessageBox.information(self, "Succès", "Sondeur supprimé avec succès!")

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QLabel, QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.models import Essai
from .forms import EssaiForm


class EssaiView(QWidget):
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
        
        title = QLabel("Gestion des Essais")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Action buttons
        self.add_button = QPushButton("➕ Nouvel Essai")
        self.edit_button = QPushButton("✏️ Modifier")
        self.delete_button = QPushButton("🗑️ Supprimer")
        
        self.add_button.clicked.connect(self.add_essai)
        self.edit_button.clicked.connect(self.edit_essai)
        self.delete_button.clicked.connect(self.delete_essai)
        
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
        essais = self.session.query(Essai).order_by(Essai.name).all()
        
        for essai in essais:
            item = QListWidgetItem()
            item.setText(f"{essai.name}")
            item.setData(Qt.UserRole, essai.id)
            
            # Add subtitle with description
            if essai.description:
                item.setText(f"{essai.name}\n📝 {essai.description}")
            
            self.list_widget.addItem(item)
    
    def on_selection_changed(self):
        has_selection = bool(self.list_widget.selectedItems())
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
    
    def add_essai(self):
        form = EssaiForm(self)
        if form.exec_() == form.Accepted:
            data = form.get_data()
            essai = Essai(**data)
            self.session.add(essai)
            self.session.commit()
            self.refresh_list()
            QMessageBox.information(self, "Succès", f"Essai '{data['name']}' ajouté avec succès!")
    
    def edit_essai(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            return
        
        essai_id = current_item.data(Qt.UserRole)
        essai = self.session.get(Essai, essai_id)
        
        form = EssaiForm(self, essai)
        if form.exec_() == form.Accepted:
            data = form.get_data()
            essai.name = data['name']
            essai.description = data['description']
            self.session.commit()
            self.refresh_list()
            QMessageBox.information(self, "Succès", "Essai modifié avec succès!")
    
    def delete_essai(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            return
        
        essai_id = current_item.data(Qt.UserRole)
        essai = self.session.get(Essai, essai_id)
        
        reply = QMessageBox.question(
            self, "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer l'essai '{essai.name}' ?\n\nCette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.session.delete(essai)
            self.session.commit()
            self.refresh_list()
            QMessageBox.information(self, "Succès", "Essai supprimé avec succès!")

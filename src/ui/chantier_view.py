from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QLabel, QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.models import Chantier
from .forms import ChantierForm


class ChantierView(QWidget):
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
        
        title = QLabel("Gestion des Chantiers")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Action buttons
        self.add_button = QPushButton("➕ Nouveau Chantier")
        self.edit_button = QPushButton("✏️ Modifier")
        self.delete_button = QPushButton("🗑️ Supprimer")
        
        self.add_button.clicked.connect(self.add_chantier)
        self.edit_button.clicked.connect(self.edit_chantier)
        self.delete_button.clicked.connect(self.delete_chantier)
        
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
        chantiers = self.session.query(Chantier).order_by(Chantier.name).all()
        
        for chantier in chantiers:
            item = QListWidgetItem()
            item.setText(f"{chantier.name}")
            item.setData(Qt.UserRole, chantier.id)
            
            # Add subtitle with location and date
            subtitle_parts = []
            if chantier.location:
                subtitle_parts.append(f"📍 {chantier.location}")
            if chantier.date:
                subtitle_parts.append(f"📅 {chantier.date.strftime('%d/%m/%Y')}")
            
            if subtitle_parts:
                item.setText(f"{chantier.name}\n{' • '.join(subtitle_parts)}")
            
            self.list_widget.addItem(item)
    
    def on_selection_changed(self):
        has_selection = bool(self.list_widget.selectedItems())
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
    
    def add_chantier(self):
        form = ChantierForm(self)
        if form.exec_() == form.Accepted:
            data = form.get_data()
            chantier = Chantier(**data)
            self.session.add(chantier)
            self.session.commit()
            self.refresh_list()
            QMessageBox.information(self, "Succès", f"Chantier '{data['name']}' ajouté avec succès!")
    
    def edit_chantier(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            return
        
        chantier_id = current_item.data(Qt.UserRole)
        chantier = self.session.get(Chantier, chantier_id)
        
        form = ChantierForm(self, chantier)
        if form.exec_() == form.Accepted:
            data = form.get_data()
            chantier.name = data['name']
            chantier.location = data['location']
            chantier.date = data['date']
            self.session.commit()
            self.refresh_list()
            QMessageBox.information(self, "Succès", "Chantier modifié avec succès!")
    
    def delete_chantier(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            return
        
        chantier_id = current_item.data(Qt.UserRole)
        chantier = self.session.get(Chantier, chantier_id)
        
        reply = QMessageBox.question(
            self, "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer le chantier '{chantier.name}' ?\n\nCette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.session.delete(chantier)
            self.session.commit()
            self.refresh_list()
            QMessageBox.information(self, "Succès", "Chantier supprimé avec succès!")

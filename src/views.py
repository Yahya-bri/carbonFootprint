# This file has been replaced by the modular UI structure in src/ui/
# The new architecture separates views into individual modules:
# - src/ui/main_window.py
# - src/ui/sondeur_view.py  
# - src/ui/essai_view.py
# - src/ui/chantier_view.py
# - src/ui/affectation_view.py
# - src/ui/forms.py

# For backward compatibility, this import redirects to the new main window
from src.ui.main_window import MainWindow

__all__ = ['MainWindow']

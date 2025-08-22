from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.db import init_db, get_session
import sys

def main():
    init_db()
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Planificateur de Tâches - Sondeurs")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Sondage Manager")
    
    session = get_session()
    win = MainWindow(session)
    win.show()
    
    try:
        app.exec_()
    finally:
        session.close()

if __name__ == '__main__':
    main()

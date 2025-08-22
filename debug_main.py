#!/usr/bin/env python3
"""Simplified main.py for debugging"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

def main():
    print("Starting application...")
    app = QApplication(sys.argv)
    print("QApplication created")
    
    # Try to create a simple window instead of our complex one
    window = QMainWindow()
    window.setWindowTitle("Debug - Simple Window")
    window.setGeometry(100, 100, 400, 300)
    
    label = QLabel("Application is working!")
    window.setCentralWidget(label)
    
    print("Simple window created")
    window.show()
    print("Window shown")
    
    # Now try to import our modules one by one
    try:
        from src.db import get_session
        print("Database import successful")
        session = get_session()
        print("Database session created")
        
        from src.ui.main_window import MainWindow
        print("MainWindow import successful")
        
        # Replace the simple window with our main window
        window.close()
        main_window = MainWindow(session)
        print("MainWindow instance created")
        main_window.show()
        print("MainWindow shown")
        
    except Exception as e:
        print(f"Error during initialization: {e}")
        import traceback
        traceback.print_exc()
    
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())

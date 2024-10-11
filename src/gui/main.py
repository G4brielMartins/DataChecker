from PySide6.QtWidgets import QApplication

from .main_components.MainWindow import MainWindow

def main():
    app = QApplication([])
    mw = MainWindow()
    mw.show()
    app.exec()
    
if __name__ == "__main__":
    main()
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class Mensagem:
    def __init__(self, main_window):
        self.label = QLabel("Carregue um ou mais arquivos para iniciar")
        self.label.setAlignment(Qt.AlignCenter)
        self.set_text("Carregue um ou mais arquivos para iniciar", "blue")

    def set_text(self, text, color="green"):
        self.label.setText(text)
        self.label.setStyleSheet(f"font-size: 18px; color: {color};")

    def show_success_message(self):
        self.set_text("Arquivo selecionado com sucesso. Escolha o gráfico para visualizar os dados.")

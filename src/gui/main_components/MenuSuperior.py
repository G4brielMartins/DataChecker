from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QAction

class MenuSuperior(QMenuBar):
    def __init__(self, main_window):
        super().__init__(main_window)

        # Opção "Menu" com subopções
        main_menu = self.addMenu('Menu')
        
        # Subopção "Selecionar Arquivos"
        select_action = QAction('Selecionar Arquivos', self)
        select_action.triggered.connect(main_window.file_manager.open_file_dialog)
        main_menu.addAction(select_action)

        # Subopção "Retornar" para resetar a interface
        reset_action = QAction('Retornar', self)
        reset_action.triggered.connect(main_window.file_manager.reset_interface)
        main_menu.addAction(reset_action)
        
        # Opção "Gráficos" para acessar os gráficos no menu superior
        main_window.graph_menu = self.addMenu('Gráficos')
        main_window.graph_menu.setEnabled(False)
        main_window.graph_menu.aboutToShow.connect(main_window.graph_manager.show_graph_options)

        # Opção "Escolher Arquivo" para seleção de arquivos carregados
        main_window.file_menu = self.addMenu('Escolher Arquivo')
        main_window.file_menu.setEnabled(False)
        main_window.file_menu.aboutToShow.connect(main_window.file_manager.populate_file_menu)

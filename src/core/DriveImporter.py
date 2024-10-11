import os

from gdown import download_folder

def drive_importer(url: str, *, out_folder: str = "Dados", quiet: bool = True) -> str:
    """
    Importa uma pasta do Google Drive para o diretório local 'Dados/'.

    Parameters
    ----------
    url : str
        Link da pasta do Google Drive.
        * O arquivo deve estar com acesso 'Qualquer pessoa com o link'
    """
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    
    raiz = os.getcwd()
    os.chdir(out_folder)
    paths = download_folder(url, quiet=quiet)
    os.chdir(raiz)

    folder_path = os.path.dirname(os.path.abspath(paths[0]))

    return folder_path
"""
Biblioteca para plot e verificação de integridade de dados gerados com o firmware ActVib.
"""

import os
from typing import Optional, TypeAlias

import numpy as np
import pandas as pd

from ActVibModules.ActVibSystem import ActVibData
from ActVibModules.Adaptive import FIRNLMS
from ActVibModules.DSPFuncs import easyFourier

Atuador: TypeAlias = int

def atuadores_disponiveis(data: ActVibData | pd.DataFrame) -> list[Atuador]:
    """
    Identifica quais atuadores apresentam dados disponíveis.

    Parameters
    ----------
    data : ActVibData or pd.DataFrame
        Dados de vibração já importados importados.

    Returns
    -------
    list[Atuador]
        
    """
    dac_columns = [name.startswith('dac') for name in data.columns]
    dac_data = data.loc[:, dac_columns]
    
    dac_indices = np.array(range(1, len(dac_data.columns) + 1))
    
    return dac_indices[dac_data.any()]

print(atuadores_disponiveis(ActVibData('data/R1_A12_0.15.feather')))

class ConfigError(Exception):
    # Erro utilizado pela classe DataHandler
    def __init__(self, path: str|os.PathLike):
        mensagem = "O objeto não está configurado. Defina o dac e imu de interesse utilizando (self.set_config)."
        super().__init__(mensagem)


class DataHandler():
    def __init__(self, path:str|os.PathLike, *, dac:Optional[str]= None, imu:Optional[str]= None):
        """
        Classe para armazenar informações referentes ao grupo de dados e facilitar sua manipulação.

        Parameters
        ----------
        path : str | os.PathLike
            Caminho do arquivo feather que contém os dados.
        dac : Optional[str], optional
            dac de interesse na análise
        imu : Optional[str], optional
            imu e a variável de interesse na análise - Ex.: 'imu2accz'
        
        * dac e imu podem ser fornecidos posteriormentes com set_config.
          Algumas funções ficam desabilitadas até a devida configuração do dac e imu.
        """
        self.name = os.path.basename(path)
        self.data = ActVibData(path)
        self.dac = dac
        self.imu = imu
    
    def is_config(self) -> bool:
        """
        Verifica se dac e imu estão configurados.

        Returns
        -------
        bool
            True se está configurado.
        """        
        return False if None in [self.dac, self.imu] else True

    def set_config(self, dac:Optional[str]= None, imu:Optional[str]= None) -> None:
        """
        Atribui valores ao dac e imu.

        Parameters
        ----------
        dac : Optional[str], optional
            Novo dac a ser utilizado.
        imu : Optional[str], optional
            Novos imu e variável a serem utilizados.
        """        
        if dac is not None:
            self.dac = dac
        if imu is not None:
            self.imu = imu
    
    def generate_fir(self) -> None:
        """
        Calcula a resposta ao impulso e armazena em (self.fir).
        * dac e imu precisam estar configurados.
        """                
        if self.is_config():
                self.fir = FIRNLMS(memorysize=2000)
                x = self.data[self.dac].values - self.data[self.dac].mean()
                y = self.data[self.imu].values - self.data[self.imu].mean()
                self.fir.run(x,y)
        else:
            raise ConfigError
    
    def generate_fir_freq(self) -> None:
        """
        Calcula a resposta ao impulso no domínio da frequência e armazena em (self.fir_freq).
        * dac e imu precisam estar configurados.
        """
        try:
            self.fir_freq = easyFourier(self.fir.ww,fs=416)
        except AttributeError:
            self.generate_fir()
            self.generate_fir_freq()


def drive_importer(url: str, *, out_folder: str = "Dados", quiet: bool = True) -> str:
    """
    Importa uma pasta do Google Drive para o diretório local 'Dados/'.

    Parameters
    ----------
    url : str
        Link da pasta do Google Drive.
        * O arquivo deve estar com acesso 'Qualquer pessoa com o link'
    """
    from gdown import download_folder
    
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    
    raiz = os.getcwd()
    os.chdir(out_folder)
    paths = download_folder(url, quiet=quiet)
    os.chdir(raiz)

    folder_path = os.path.dirname(os.path.abspath(paths[0]))

    return folder_path
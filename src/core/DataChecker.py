"""
Módulo para plot e verificação de integridade de dados gerados com o firmware ActVib.
"""
from typing import Optional, TypeAlias, Tuple, Sequence

import numpy as np
import pandas as pd

from ActVibModules.ActVibSystem import ActVibData
from ActVibModules.Adaptive import FIRNLMS
from ActVibModules.DSPFuncs import easyFourier

Atuador: TypeAlias = str
Amplitude: TypeAlias = float
Tempo: TypeAlias = float
Hz: TypeAlias = float

def atuadores_disponiveis(data: ActVibData | pd.DataFrame) -> Tuple[Atuador]:
    """
    Identifica quais atuadores apresentam dados disponíveis.

    Parameters
    ----------
    data : ActVibData | pd.DataFrame
        Dados de vibração já importados importados.

    Returns
    -------
    Tuple[Atuador]
        Lista com os atuadores disponíveis para acesso - ['dac1', 'dac2'].
    """
    dac_columns = np.array([name for name in data.columns if name.startswith('dac')])
    dac_data = data.loc[:, dac_columns]
    
    dacs_disponiveis = dac_columns[dac_data.any()]
    
    return dacs_disponiveis


def get_ir(resposta: Sequence[float], estimulo: Sequence[float], amostragem: Optional[Hz] = None, 
            *, memorysize: int = 2000, **firlms_kwargs) -> Tuple[Amplitude, Tempo]:
    """Calcula a resposta ao impulso da (resposta) em função do (estímulo).

    Parameters
    ----------
    resposta : Sequence[float]
        Sinal de saída do sistema.
    estimulo : Sequence[float]
        Sinal de entrada do sistema.
    amostragem : float, optional
        Frequência de amostragem dos dados em Hz.
        Por padrão retorna o índice numérico da amostra.
    frlms_kwargs : optional
        Argumentos extras para a função FIRLMS.

    Returns
    -------
    Tuple[Amplitude, Tempo]
        Par Amplitude x Tempo que compõe a resposta ao impulso do sistema.
    """
    fir = FIRNLMS(memorysize=memorysize, **firlms_kwargs)
    x: list[float] = estimulo - np.mean(estimulo)
    y: list[float] = resposta - np.mean(resposta)
    fir.run(x,y)
    
    time_index: list[float] = np.array(range(len(fir.ww))) / amostragem
    
    return fir.ww, time_index


def get_fr_from_ir(ir: list[Amplitude, Tempo]) -> Tuple[Amplitude, Hz]:
    """Calcula a resposta em frequência de uma resposta ao impulso.
    Define a frequência de amostragem a partir do período entre amostras.

    Parameters
    ----------
    ir : list[Amplitude, Tempo]
        Amplitudes da resposta ao impulso.

    Returns
    -------
    list[Amplitude, Hz]
        _description_
    """
    amostragem = 1.0 / (ir[1][1] - ir[1][0])
    
    return easyFourier(np.array(ir[0]), fs=amostragem)


def get_fr(resposta: Sequence[float], estimulo: Sequence[float], amostragem: Hz, 
            *, memorysize: int = 2000, **firlms_kwargs) -> Tuple[Amplitude, Tempo]:
    """Calcula a resposta em frequência da (resposta) em função do (estímulo).

    Parameters
    ----------
    resposta : Sequence[float]
        Sinal de saída do sistema.
    estimulo : Sequence[float]
        Sinal de entrada do sistema.
    amostragem : float, optional
        Frequência de amostragem dos dados em Hz.
    frlms_kwargs : optional
        Argumentos extras para a função FIRLMS.

    Returns
    -------
    list[Amplitude, Hz]
        Par Amplitude x Frequência que compõe a resposta ao impulso do sistema.
    """
    ir = get_ir(resposta, estimulo, amostragem, memorysize=memorysize, **firlms_kwargs)
    
    return get_fr_from_ir(ir)
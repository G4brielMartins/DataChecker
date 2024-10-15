import os
from typing import Optional, TypeAlias, overload

import numpy as np
from ActVibModules.ActVibSystem import ActVibData

from . import Utils as ut

Atuador_DAC: TypeAlias = int
Sensor_IMU: TypeAlias = int

FREQ = 416

def Singleton(cls):
    instances = {}
    def instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return instance


class FileEntry:
    def __init__(self, file_path: str) -> None:
        self.path = file_path
        self.name = os.path.basename(file_path)
        self.data = ActVibData(file_path)
        self.dacs = ut.dacs_disponiveis(self.data)
        self.imus = ut.imus_disponiveis(self.data)
        
        self.selected_sens = self.data[f"imu{self.imus[0]}accz"]
        self.selected_dac = self.data[f"dac{self.dacs[0]}"]
        self.graphs = {}
    
    def get_graph(self, graph: str):
        if graph not in self.graphs:
            match graph:
                case "scatter":
                    y = self.selected_sens
                    x = list(range(len(y)))
                    self.graphs["scatter"] = [x, y]
                case "ir":
                    y, x = ut.get_ir(self.selected_sens, self.selected_dac, FREQ)
                    self.graphs["ir"] = [x, y]
                case "fr":
                    y, x = ut.get_fr(self.selected_sens, self.selected_dac, FREQ)
                    self.graphs["fr"] = [x, y]
        return self.graphs[graph]
    
    def set_config(self, dac: Optional[int] = None, imu: Optional[int] = None, sens: Optional[str] = None):
        input = np.array([dac, imu, sens]) != None
        if input[0]:
            self.selected_dac = self.data[f"dac{dac}"]
        if any(input[1:]):
            self.selected_sens = self.data["imu" + imu + sens]
        if any(input):
            self.graphs.clear()

@Singleton
class FileManager:
    def __init__(self) -> None:
        self.files = {}
    
    @overload
    def __getitem__(self, key: str|int) -> FileEntry: ...
    @overload
    def __getitem__(self, key: slice) -> list[FileEntry]: ...
    def __getitem__(self, key):
        match key:
            case str():
                return self.files[key]
            case int() | slice():
                return list(self.files.values())[key]
    
    def __len__(self) -> int:
        return len(self.files.values())
    
    def count_files(self) -> int:
        return len(self)
    
    def add_files(self, file_paths: str|list[str]) -> None:
        if isinstance(file_paths, list):
            for path in file_paths:
                self.add_files(path)
        elif file_paths not in self.files:
            self.files[file_paths] = FileEntry(file_paths)
    
    def remove_files(self, file_paths: str|list[str]) -> None:
        if isinstance(file_paths, list):
            for path in file_paths:
                self.remove_files(path)
        elif file_paths in self.files:
            self.files.pop(file_paths)
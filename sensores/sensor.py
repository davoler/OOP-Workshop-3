import sys
import os

# Asegura que se pueda importar desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
                                             
# sensor.py
from Sistemas.base_subsystem import BaseSubsystem
import random

class Gyroscope(BaseSubsystem):
    def __init__(self, name: str = "Gyroscope"):
        super().__init__(name)
    
    def initialize(self):
        pass

    def update(self, dt):
        pass

    def read_data(self):
        return {
            "omega_x": round(random.uniform(-0.01, 0.01), 4),
            "omega_y": round(random.uniform(-0.01, 0.01), 4),
            "omega_z": round(random.uniform(-0.01, 0.01), 4)
        }

class SunSensor(BaseSubsystem):
    def __init__(self, name: str = "SunSensor"):
        super().__init__(name)
    
    def initialize(self):
        pass

    def update(self, dt):
        pass

    def read_data(self):
        # Simula ángulo hacia el Sol en elevación y azimut
        elevation = round(random.uniform(-90, 90), 2)
        azimuth = round(random.uniform(0, 360), 2)
        return {
            "sun_elevation": elevation,
            "sun_azimuth": azimuth
        }
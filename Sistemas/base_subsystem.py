from abc import ABC, abstractmethod

class BaseSubsystem(ABC):
    
    def __init__(self, name: str):
        
        self.name = name
        self.active = True 

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass
    
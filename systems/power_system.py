from base_subsystem import BaseSubsystem

class PowerSystem(BaseSubsystem):
    def __init__(self):
        BaseSubsystem.__init__(self, "Power System")

        # Atributos específicos de este subsistema
        self.battery_level = 100.0        # en porcentaje (%)
        self.solar_input = 20.0           # energía generada por segundo (W)
        self.consumption_rate = 15.0      # energía consumida por segundo (W)
        self.in_eclipse = False           # True si no hay sol (eclipse)

    def initialize(self):
        print(f"[{self.name}] Inicializado con batería al {self.battery_level}%.")

    def update(self, dt):
        """
        Simula la carga o descarga de la batería según si hay eclipse o no.
        """
        if self.in_eclipse:
            generated = 0.0
        else:
            generated = self.solar_input * dt

        consumed = self.consumption_rate * dt
        delta_energy = (generated - consumed) / 100.0  # cambio porcentual

        self.battery_level += delta_energy
        self.battery_level = max(0.0, min(100.0, self.battery_level))  # limitar entre 0 y 100

        if self.battery_level <= 20.0:
            self.active = False
            print(f"[{self.name}] Nivel crítico de batería. Sistema desactivado.")
        elif not self.active and self.battery_level > 20.0:
            self.active = True
            print(f"[{self.name}] Sistema reactivado.")

    def set_eclipse(self, state: bool):
        """
        Cambia el estado de eclipse (True = sin luz solar).
        """
        self.in_eclipse = state

import sys
import os

# La siguiente linea la dio chatgpt, sirve como una forma de forzar a python 
# de encontrar el camino ya que no tomaba a Sistemas como un modulo. 
# Los anteriores import se hicieron para que esa linea funcionara.

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos la clase base con los metodos que todos los subsistemas están implementando.
from Sistemas.base_subsystem import BaseSubsystem

class TermalCam(BaseSubsystem):
    def __init__(self, name: str = "Termal Camera"):
        super().__init__(name)
        self.state = "idle"
        self.temperature = 25.0     # temperatura inicial de la cámara (°C)
        self.cooldown_rate = 0.033  # tasa de enfriamiento (°C/s) en eclipse. Originalmente se definió de 5 °C/min
        self.heatup_rate = 0.016    # tasa de calentamiento (°C/s) en luz solar. Tambien e definió de 5 °C/min
        self.generated_data = []    # pa guardar las imágenes
        self.elapsed_time = 0       # pa registrar el tiempo desde el inicio de la simulación

    def initialize(self):
        print(f"{self.name} initialized.")
        self.state = "idle"
        self.temperature = 25.0
        self.generated_data.clear()
        self.elapsed_time = 0

    def update(self, dt: float, battery_level: float, in_eclipse: bool, orientation_ok: bool = True):
    #estas variables se toman igual que las usadas en el powe system y sensor system
        self.elapsed_time += dt
        if in_eclipse:
            self.temperature = max(self.temperature - self.cooldown_rate * dt, -100)
        else:
            self.temperature = min(self.temperature + self.heatup_rate * dt, 100)
          if int(self.elapsed_time) % 600 != 0:
            self.state = "idle"
            return

        if battery_level < 20:
            self.state = "low_power"
            return

        if not orientation_ok:
            self.state = "bad_orientation"
            return

        if self.temperature > 85:
            self.state = "overheated"
            return

        if self.temperature < -40:
            self.state = "overcooled"
            return
        
        # ✅ Todo está bien → capturar imagen
        self.state = "active"
        image_id = f"img_t{int(self.elapsed_time)}_T{round(self.temperature, 1)}"
        self.generated_data.append(image_id)
        print(f"{self.name} captured image: {image_id}")

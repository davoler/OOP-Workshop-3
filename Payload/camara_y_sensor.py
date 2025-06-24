import sys
import os

# La siguiente linea la dio chatgpt, sirve como una forma de forzar a python 
# de encontrar el camino ya que no tomaba a Sistemas como un modulo. 
# Los anteriores import se hicieron para que esa linea funcionara.

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos la clase base con los metodos que todos los subsistemas están implementando.
from Sistemas.base_subsystem import BaseSubsystem


#####
#DEFINO CÁMARA TÉRMICA
#####
class TermalCam(BaseSubsystem):
    def __init__(self, name: str = "Termal Camera"):
        super().__init__(name)
        self.state = "idle"
        self.temperature = 25.0     # temperatura inicial de la cámara (°C)
        self.cooldown_rate = 0.0833  # tasa de enfriamiento (°C/s) en eclipse. Originalmente se definió de 5 °C/min
        self.heatup_rate = 0.0833    # tasa de calentamiento (°C/s) en luz solar. Tambien e definió de 5 °C/min
        self.generated_data = []    # pa guardar las imágenes
        self.elapsed_time = 0       # pa registrar el tiempo desde el inicio de la simulación

    def initialize(self):
        print(f"{self.name} initialized.")
        self.state = "idle"
        self.temperature = 25.0
        self.generated_data.clear()
        self.elapsed_time = 0

    def update(self, dt: float, battery_level: float, in_eclipse: bool, orientation_ok: bool = True):
    #estas variables son iguales que las usadas en el power system y sensor system
        self.elapsed_time += dt
        if in_eclipse:
            self.temperature = max(self.temperature - self.cooldown_rate * dt, -100)
        else:
            self.temperature = min(self.temperature + self.heatup_rate * dt, 100)
        if int(self.elapsed_time) % 600 != 0: #Toma de fotos cada 10 min
            self.state = "idle"
            return

        if battery_level < 20:                  #si tiene menos de 20 % de bateria se desactiva
            self.state = "Sistema desactivado"
            return

        if not orientation_ok:                  #Para definir la posicion
            self.state = "bad_orientation"      ####### Tengo que decirle a angie cuadno termine lo de ella
            return

        if self.temperature > 80:               #las siguientes dos entradas es para cuidar el rango de temperatura en que funciona
            self.state = "overheated"
            return

        if self.temperature < -40:
            self.state = "overcooled"
            return
        #El codigo a continuacion busca crear un ID unico para cada imagen, lo guarda segun tiempo y temperatura, y lo que imprime es la imagen capturada
        self.state = "active"
        image_id = f"img_t{int(self.elapsed_time)}_T{round(self.temperature, 1)}"
        self.generated_data.append(image_id)
        print(f"{self.name} captured image: {image_id}")


#####
#DEFINO EL SENSOR DE TEMPERATURA
#####


class TempSensor(BaseSubsystem):
    def __init__(self, name: str = "Temperature Sensor"):
        super().__init__(name)
        self.state = "idle"
        self.environment_temp = 25.0
        self.cooldown_rate = 0.0833  # °C/s igual que el de la cámara
        self.heatup_rate = 0.0833
        self.generated_data = []
        self.elapsed_time = 0

    def initialize(self):
        print(f"{self.name} initialized.")
        self.state = "idle"
        self.generated_data.clear()
        self.elapsed_time = 0
        self.environment_temp = 25.0

    def update(self, dt: float, battery_level: float, in_eclipse: bool):
        if self.failed:
            self.state = "failed"
            return

        self.elapsed_time += dt

        # Nueva lógica térmica igual a TermalCam
        if in_eclipse:
            self.environment_temp = max(self.environment_temp - self.cooldown_rate * dt, -100)
        else:
            self.environment_temp = min(self.environment_temp + self.heatup_rate * dt, 100)

        # Batería baja: apagado
        if battery_level < 20:
            self.state = "low_power"
            return

        # Falla permanente por frío extremo
        if self.environment_temp < -50:
            self.state = "Overcooled"
            return

        self.state = "active"
        reading = {"time": round(self.elapsed_time), "temperature": round(self.environment_temp, 2)}
        self.generated_data.append(reading)
        print(f"{self.name} reading: {reading}")


#####
#Pa que sea facil usar todo esto desde el archivo de la simulación, hay que hacer otra clase que es la que se va a llamar
#####

class PayloadSystem(BaseSubsystem):
    def __init__(self):
        super().__init__("Payload System")
        self.camera = TermalCam()
        self.sensor = TempSensor()

    def initialize(self):
        self.camera.initialize()
        self.sensor.initialize()

    def update(self, dt: float, battery_level: float, in_eclipse: bool, orientation_ok: bool):
        self.camera.update(dt, battery_level, in_eclipse, orientation_ok)
        self.sensor.update(dt, battery_level, in_eclipse)
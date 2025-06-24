import matplotlib.pyplot as plt
from Sistemas.base_subsystem import BaseSubsystem
from Power.power_system import PowerSystem
from Communications.communication_system import CommunicationSystem

class SatelliteSimulator:
    def __init__(self):
        self.subsystems = []

    def register_subsystem(self, subsystem: BaseSubsystem):
        self.subsystems.append(subsystem)
        subsystem.initialize()
        print(f"[Simulador] Registrado: {subsystem.name}")

    def run(self, duration, dt=1.0):
        print(f"\n🚀 Iniciando simulación por {duration} segundos...\n")

        power = next((s for s in self.subsystems if isinstance(s, PowerSystem)), None)
        comm = next((s for s in self.subsystems if isinstance(s, CommunicationSystem)), None)
        history = {"t": [], "battery": [], "buffer": []}

        for t in range(duration):
            print(f"\n⏱️ Tiempo: {t}s")

            if comm:
                comm.set_window(t % 15 < 7)  # ventana abierta 7 de cada 15 s

            for s in self.subsystems:
                s.update(dt)

            history["t"].append(t)
            if power:
                history["battery"].append(power.battery_level)
            if comm:
                history["buffer"].append(len(comm.buffer))

        self.plot(history)

    def plot(self, history):
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(history["t"], history["battery"])
        plt.title("Nivel de batería")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("%")

        plt.subplot(1, 2, 2)
        plt.plot(history["t"], history["buffer"])
        plt.title("Mensajes en buffer")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Cantidad")
        plt.tight_layout()
        plt.show()

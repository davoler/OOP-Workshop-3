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
        print(f"[Simulador] Subsistema '{subsystem.name}' registrado.")

    def run(self, duration, dt=1.0):
        print(f"\n🚀 Iniciando simulación por {duration} segundos...\n")

        # Para guardar datos de la simulación
        history = {"t": [], "battery": [], "buffer": []}

        # Detectar subsistemas clave
        power = next((s for s in self.subsystems if isinstance(s, PowerSystem)), None)
        comm = next((s for s in self.subsystems if isinstance(s, CommunicationSystem)), None)

        for t in range(duration):
            print(f"\n⏱️ Tiempo: {t}s")

            # Control de ventana de comunicación
            if comm:
                comm.set_window(t % 15 < 7)  # ventana abierta 7 de cada 15 segundos

            # Actualizar subsistemas
            for subsystem in self.subsystems:
                subsystem.update(dt)

            # Guardar estado para graficar
            history["t"].append(t)
            if power:
                history["battery"].append(power.battery_level)
            if comm:
                history["buffer"].append(len(comm.buffer))

        # Mostrar gráficas al final
        self.plot_results(history)

    def plot_results(self, history):
        plt.figure(figsize=(10, 5))

        if "battery" in history:
            plt.subplot(1, 2, 1)
            plt.plot(history["t"], history["battery"], label="Nivel de batería")
            plt.xlabel("Tiempo (s)")
            plt.ylabel("Batería (%)")
            plt.title("Evolución de batería")
            plt.grid(True)

        if "buffer" in history:
            plt.subplot(1, 2, 2)
            plt.plot(history["t"], history["buffer"], label="Buffer de mensajes", color="orange")
            plt.xlabel("Tiempo (s)")
            plt.ylabel("Cantidad de mensajes")
            plt.title("Mensajes acumulados")
            plt.grid(True)

        plt.tight_layout()
        plt.show()

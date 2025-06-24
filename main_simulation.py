from Power.power_system import PowerSystem
from Communications.communication_system import CommunicationSystem
from simulator import SatelliteSimulator

def main():
    sim = SatelliteSimulator()

    # Crear subsistemas
    power = PowerSystem()
    comm = CommunicationSystem()

    # Enlazar subsistemas
    power.comm_system = comm
    comm.power_system = power

    # Registrar en simulador
    sim.register_subsystem(power)
    sim.register_subsystem(comm)

    # Ejecutar simulación
    sim.run(duration=60)

if __name__ == "__main__":
    main()

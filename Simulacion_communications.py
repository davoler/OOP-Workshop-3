#Simulación del subsistema de comunicaciones

from Communications.communication_system import CommunicationSystem

comm = CommunicationSystem()
comm.initialize()
comm.set_window(True)

# Simulamos otros sistemas enviando info
comm.receive_data("Nivel batería: 83%")
comm.receive_data("Modo: Eclipse")
comm.receive_data("Temperatura estable")

# Simulación de 10 segundos
for t in range(1, 11):
    comm.update(dt=1.0)
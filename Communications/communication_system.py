from Sistemas.base_subsystem import BaseSubsystem

class CommunicationSystem(BaseSubsystem):
    def __init__(self):
        super().__init__("Communication System")

        # Mensajes acumulados para enviar
        self.buffer = []

        # Parámetros del sistema
        self.data_rate = 1.0  # mensajes por segundo
        self.energy_per_message = 0.5  # unidad de energía por mensaje
        self.transmitting = False
        self.window_open = False  # Indica si hay ventana de comunicación

    def initialize(self):
        print(f"[{self.name}] Sistema de comunicaciones inicializado.")

    def update(self, dt):
        if not self.active or not self.window_open:
            self.transmitting = False
            return

        messages_to_send = int(self.data_rate * dt)
        sent = 0

        for _ in range(messages_to_send):
            if self.buffer:
                msg = self.buffer.pop(0)
                sent += 1
                print(f"[{self.name}] Enviando mensaje: {msg}")
            else:
                break

        if sent > 0:
            self.transmitting = True
        else:
            self.transmitting = False

    def receive_data(self, message: str):
        """Llamado por otros subsistemas para agregar datos a enviar"""
        self.buffer.append(message)

    def set_window(self, open: bool):
        """Activa o desactiva la ventana de comunicación con la Tierra"""
        self.window_open = open
        

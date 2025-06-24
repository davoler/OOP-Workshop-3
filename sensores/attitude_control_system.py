# attitude_control_system.py

class AttitudeControlSystem:
    def __init__(self, sensors, actuator):
        self.__orientation = [0.0, 0.0, 0.0]  # Roll, pitch, yaw
        self.sensors = sensors               
        self.actuator = actuator

    def update_attitude(self):
        print(" Lectura de sensores:")
        all_data = []
        for sensor in self.sensors:
            data = sensor.read_data()
            print(f" - {sensor.__class__.__name__}: {data}")
            all_data.append(data)
        return all_data

    def apply_control(self, desired_orientation):
        print(f" Objetivo: {desired_orientation}")
        error = [desired_orientation[i] - self.__orientation[i] for i in range(3)]
        print(f"🔧 Error calculado: {error}")
        self.actuator.apply_torque(error)
        self.__orientation = desired_orientation

    def get_status(self):
        return {"orientación_actual": self.__orientation}

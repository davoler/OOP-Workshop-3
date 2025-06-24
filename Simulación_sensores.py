from sensores.sensor import Gyroscope, SunSensor
from sensores.actuator import Actuator
from sensores.attitude_control_system import AttitudeControlSystem

if __name__ == "__main__":
    # Crear sensores y actuador
    gyro = Gyroscope()
    sun = SunSensor()
    actuator = Actuator()

    # Sistema de control de actitud
    adcs = AttitudeControlSystem([gyro, sun], actuator)

    # Simular 10 ciclos
    for ciclo in range(1, 11):
        print(f"\n Ciclo de simulación #{ciclo}")
        adcs.update_attitude()
        adcs.apply_control([0.05 * ciclo, -0.02 * ciclo, 0.03 * ciclo])
        estado = adcs.get_status()
        print(f"✅ Estado actual: {estado}")
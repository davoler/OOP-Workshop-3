from Payload.camara_y_sensor import PayloadSystem
from Power.power_system import PowerSystem
from sensores.attitude_control_system import AttitudeControlSystem
from sensores.sensor import Gyroscope, SunSensor
from sensores.actuator import Actuator

# Instancias de subsistemas
power = PowerSystem()
payload = PayloadSystem()
gyro = Gyroscope()
sun_sensor = SunSensor()
actuator = Actuator()
attitude = AttitudeControlSystem([gyro, sun_sensor], actuator)

# Inicializar
power.initialize()
payload.initialize()
gyro.initialize()
sun_sensor.initialize()

# Parámetros de simulación
dt = 60  # 60 segundos
total_time = 3600
steps = total_time // dt

# ⚙️ Control proporcional suave
Kp = 0.3  # Ganancia para que la corrección sea progresiva

for step in range(int(steps)):
    current_time = step * dt

    # Eclipse alternado cada 10 min
    in_eclipse = (current_time // 600) % 2 == 1
    power.set_eclipse(in_eclipse)

    # 🔋 Actualizar batería
    power.update(dt)
    battery_level = power.battery_level

    # 🛰️ Obtener orientación
    sensor_data = attitude.update_attitude()
    orientation_ok = sensor_data[1]["sun_elevation"] > 0

    # 📷 Actualizar sensores
    payload.update(dt, battery_level, in_eclipse, orientation_ok, current_time)

    # ⚠️ Evento de impacto con escombro en el segundo 2000
    if current_time == 1680:
        attitude._AttitudeControlSystem__orientation = [5.0, -3.0, 2.0]
        print("\n⚠️ ¡Impacto con escombro! Orientación perturbada a [5.0, -3.0, 2.0]°\n")

    # 🎯 Aplicar control de actitud con ganancia suave
    desired_orientation = [0.0, 0.0, 0.0]
    current_orientation = attitude._AttitudeControlSystem__orientation
    error = [desired_orientation[i] - current_orientation[i] for i in range(3)]
    torque = [Kp * e for e in error]
    actuator_commands = actuator.apply_torque(torque)

    # Aplicar el efecto del torque a la orientación
    attitude._AttitudeControlSystem__orientation = [
        current_orientation[i] + torque[i] for i in range(3)
    ]

    # --- OUTPUT LIMPIO ---
    print(f"\n⏱️ Tiempo: {current_time}s")
    print(f"🌘 Eclipse: {in_eclipse} | 🔋 Batería: {battery_level:.1f}% | 📐 Orientación ok: {orientation_ok}")
    print(f"🛰️ Orientación actual: {[round(a, 2) for a in attitude._AttitudeControlSystem__orientation]}")
    print(f"🛠️ Torque correctivo aplicado: {[round(t, 3) for t in torque]}")

    # Mostrar imagen capturada si existe
    cam = payload.camera
    if cam.state == "active" and cam.generated_data:
        print(f"📸 Imagen capturada: {cam.generated_data[-1]}")

    # Mostrar lectura de temperatura si se genera
    temp = payload.sensor
    if temp.state == "active" and temp.generated_data:
        last_reading = temp.generated_data[-1]
        print(f"🌡️ Sensor temperatura: {last_reading}")
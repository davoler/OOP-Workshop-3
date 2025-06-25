from Payload.camara_y_sensor import PayloadSystem

payload = PayloadSystem()
payload.initialize()

# Parámetros de simulación
dt = 60  # paso de tiempo en segundos
total_simulation_time = 700  # 1 hora 
steps = total_simulation_time // dt

# Variables de entorno
battery_level = 100.0
orientation_ok = True  #por el momento que todavia ni idea de como unir esto. Solo para ver que funcione

# Simulación
for step in range(int(steps)):
    current_time = step * dt

    # eclipse cada 10 minutos
    in_eclipse = (current_time // 6000) % 2 == 1

    # consumo de batería por minuto
    battery_level -= 0.5  # lo que se va descargando
    battery_level = max(0, battery_level)

    print(f"\n--- Tiempo: {current_time}s | Batería: {battery_level:.1f}% | Eclipse: {in_eclipse} ---")

    # Ejecuta update del sistema de payloads
    payload.update(
        dt=dt,
        battery_level=battery_level,
        in_eclipse=in_eclipse,
        orientation_ok=orientation_ok,
        time_elapsed=current_time)

#Simulación del subsistema de energía con eclipse

from Power.power_system import PowerSystem
import time

# Crear e inicializar el subsistema de energía
power = PowerSystem()
power.initialize()

# Simulación por 1000 segundos (con paso de 1 segundo)
print("\n🔋 Iniciando simulación sin eclipse...")
for t in range(1, 31):  # primeros 30 segundos con sol
    power.update(dt=1.0)
    print(f"⏱️  {t:02d}s - Batería: {power.battery_level:.1f}% - Activo: {power.active}")
    time.sleep(0.05)  # para ver la salida en tiempo real

# Activar eclipse
power.set_eclipse(True)
print("\n🌑 Eclipse activado (sin generación solar)...")

for t in range(31, 500):
    power.update(dt=1.0)
    print(f"⏱️  {t:02d}s - Batería: {power.battery_level:.1f}% - Activo: {power.active}")
    time.sleep(0.05)
    
# Desactivar eclipse
power.set_eclipse(False)
print("\n☀️ Eclipse desactivado (con generación solar)...")

for t in range(500, 1000):
    power.update(dt=1.0)
    print(f"⏱️  {t:02d}s - Batería: {power.battery_level:.1f}% - Activo: {power.active}")
    time.sleep(0.05)
    
    
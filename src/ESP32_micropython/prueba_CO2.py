import network
import time
from machine import UART
from umqtt.simple import MQTTClient

# ---------------------------
# Configuración WiFi
# ---------------------------
wifi_ssid = "INFINITUM574D"
wifi_password = "Mj9Ca9Aw4k"

# ---------------------------
# Configuración del Broker MQTT
# ---------------------------
broker = "test.mosquitto.org"
port = 1883
client_id = "esp32_sensor_co2"
topic_pub = b"sensors/co2"

# ---------------------------
# Conexión WiFi
# ---------------------------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("📶 Conectando a la red WiFi:", wifi_ssid)
wlan.connect(wifi_ssid, wifi_password)

timeout = 30
start_time = time.time()
while not wlan.isconnected() and (time.time() - start_time < timeout):
    print("⏳ Conectando WiFi...")
    time.sleep(1)

if wlan.isconnected():
    print("✅ Conectado a WiFi!")
    print("📡 Configuración de red:", wlan.ifconfig())
else:
    print("❌ No se pudo conectar a WiFi")
    raise Exception("WiFi connection failed")

# ---------------------------
# Conexión al broker MQTT
# ---------------------------
try:
    print("🔌 Conectando al broker MQTT...")
    client = MQTTClient(client_id=client_id, server=broker, port=port, keepalive=60)
    client.connect()
    print("✅ Conexión MQTT exitosa!")
except Exception as e:
    print("❌ Error al conectar al broker MQTT:", e)
    raise e

# ---------------------------
# Lectura desde el sensor MH-Z19 por UART
# ---------------------------
uart = UART(2, baudrate=9600, tx=17, rx=16)  # Cambia pines si usas otros

def leer_co2():
    cmd = b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79'
    uart.write(cmd)
    time.sleep(0.1)
    if uart.any():
        resp = uart.read(9)
        if resp and len(resp) == 9:
            co2 = resp[2] * 256 + resp[3]
            return co2
    return None

# ---------------------------
# Publicar CO2 en loop
# ---------------------------
try:
    while True:
        co2 = leer_co2()
        if co2:
            msg = "CO2: {} ppm".format(co2)
            print("📤 Enviando:", msg)
            client.publish(topic_pub, msg)
        else:
            print("⚠️ Error al leer el sensor")
        time.sleep(5)
except KeyboardInterrupt:
    print("⛔ Programa detenido por el usuario.")
finally:
    client.disconnect()
    print("🔌 Desconectado del broker.")

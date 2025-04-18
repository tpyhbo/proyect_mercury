import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# -----------------------
# WiFi y MQTT config
# -----------------------
ssid = "INFINITUM574D"
password = "Mj9Ca9Aw4k"
broker = "test.mosquitto.org"
client_id = "esp32_controlador"
topics = {
    b"casa/cocina/led1": Pin(15, Pin.OUT),
    b"casa/cocina/led2": Pin(2, Pin.OUT),
    b"casa/sala/led1": Pin(4, Pin.OUT),
    b"casa/sala/led2": Pin(5, Pin.OUT),
    b"casa/sala/abanico": Pin(18, Pin.OUT),
}

# -----------------------
# Conexión WiFi
# -----------------------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
print("📶 Conectando a WiFi...")
while not wlan.isconnected():
    time.sleep(1)
print("✅ Conectado a WiFi")

# -----------------------
# Función callback MQTT
# -----------------------
def callback(topic, msg):
    print("📥 Mensaje:", topic, msg)
    if topic in topics:
        if msg == b"ON":
            topics[topic].value(1)
        elif msg == b"OFF":
            topics[topic].value(0)

# -----------------------
# Conexión al broker MQTT
# -----------------------
client = MQTTClient(client_id, broker)
client.set_callback(callback)
client.connect()
print("🔌 Conectado al broker MQTT")

# -----------------------
# Subscribirse a los tópicos
# -----------------------
for t in topics:
    client.subscribe(t)
    print("📡 Subscrito a", t)

# -----------------------
# Esperar comandos
# -----------------------
try:
    while True:
        client.check_msg()
        time.sleep(0.1)
except KeyboardInterrupt:
    client.disconnect()
    print("🔌 Desconectado del broker")

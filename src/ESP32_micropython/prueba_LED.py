import network
import time
from umqtt.simple import MQTTClient
from machine import Pin

# Configuración WiFi
wifi_ssid = "INFINITUM574D"
wifi_password = "Mj9Ca9Aw4k"

# Configuración MQTT
broker = "test.mosquitto.org"
port = 1883
client_id = "esp32_led_control"
topic_sub = b"led/control"

# Pin del LED
led = Pin(2, Pin.OUT)

# Conexión WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("📶 Conectando WiFi...")
wlan.connect(wifi_ssid, wifi_password)

while not wlan.isconnected():
    print("⏳ Esperando conexión WiFi...")
    time.sleep(1)

print("✅ Conectado a WiFi:", wlan.ifconfig())

# Función cuando llega un mensaje
def callback(topic, msg):
    print("📥 Mensaje recibido:", msg)
    if msg == b"ON":
        led.value(1)
        print("💡 LED encendido")
    elif msg == b"OFF":
        led.value(0)
        print("💡 LED apagado")

# Conectar al broker
client = MQTTClient(client_id, broker, port)
client.set_callback(callback)
client.connect()
client.subscribe(topic_sub)

print("🔌 Suscrito al tópico:", topic_sub)

try:
    while True:
        client.check_msg()
        time.sleep(1)
except KeyboardInterrupt:
    print("⛔ Finalizado por el usuario.")
finally:
    client.disconnect()

import paho.mqtt.client as mqtt

# ---------------------------
# Configuración del broker y tópicos
# ---------------------------
broker = "test.mosquitto.org"
topics = [("sensors/temp", 0), ("sensors/hum", 0), ("sensors/co2", 0)]

# ---------------------------
# Funciones callback
# ---------------------------
def on_connect(client, userdata, flags, rc):
    print("✅ Conectado al broker con código:", rc)
    for topic, qos in topics:
        client.subscribe(topic)
        print(f"📡 Suscrito al tópico '{topic}'")

def on_message(client, userdata, msg):
    print(f"📥 [{msg.topic}] → {msg.payload.decode()}")

# ---------------------------
# Inicializar cliente
# ---------------------------
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("🔌 Conectando al broker...")
client.connect(broker, 1883, 60)

print("🕵️ Escuchando mensajes...")
client.loop_forever()

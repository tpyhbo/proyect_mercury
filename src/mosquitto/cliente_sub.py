import paho.mqtt.client as mqtt

broker = "test.mosquitto.org"
topic = "sensors/co2"

# Callback cuando se conecta al broker
def on_connect(client, userdata, flags, rc):
    print("✅ Conectado al broker con código:", rc)
    client.subscribe(topic)

# Callback cuando llega un mensaje
def on_message(client, userdata, msg):
    print("📥 Mensaje recibido:", msg.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("🔌 Conectando al broker...")
client.connect(broker, 1883, 60)

print("📡 Escuchando el tópico '{}'...".format(topic))
client.loop_forever()

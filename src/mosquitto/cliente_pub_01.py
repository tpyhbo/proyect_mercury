import paho.mqtt.client as mqtt

broker = "test.mosquitto.org"
topic = "led/control"

client = mqtt.Client()

print("🔌 Conectando al broker...")
client.connect(broker, 1883, 60)

while True:
    cmd = input("💻 Escribe ON para encender o OFF para apagar el LED: ").strip().upper()
    if cmd in ["ON", "OFF"]:
        client.publish(topic, cmd)
        print("📤 Enviado:", cmd)
    elif cmd == "EXIT":
        break
    else:
        print("⚠️ Comando no válido. Usa ON, OFF o EXIT.")

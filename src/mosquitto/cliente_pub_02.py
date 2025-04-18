import paho.mqtt.client as mqtt

broker = "test.mosquitto.org"
port = 1883
client_id = "cliente_control_pc"

# 🛠️ Crear cliente con protocolo especificado (versión moderna)
client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
client.connect(broker, port, keepalive=60)
print("✅ Conectado al broker MQTT")

# Diccionario de tópicos
dispositivos = {
    "1": "casa/cocina/led1",
    "2": "casa/cocina/led2",
    "3": "casa/sala/led1",
    "4": "casa/sala/led2",
    "5": "casa/sala/abanico"
}

# Menú interactivo
print("""
Selecciona el dispositivo que quieres controlar:
1 - LED Cocina 1
2 - LED Cocina 2
3 - LED Sala 1
4 - LED Sala 2
5 - Abanico (Sala)
""")

while True:
    opcion = input("📲 Ingresa el número del dispositivo (o 'q' para salir): ")
    if opcion.lower() == "q":
        break

    if opcion in dispositivos:
        estado = input("💡 Escribe 'ON' para encender o 'OFF' para apagar: ").upper()
        if estado in ["ON", "OFF"]:
            topic = dispositivos[opcion]
            client.publish(topic, estado)
            print(f"✅ Enviado '{estado}' al tópico '{topic}'")
        else:
            print("❌ Comando no válido. Usa 'ON' o 'OFF'.")
    else:
        print("❌ Opción no válida. Intenta con un número del 1 al 5.")

client.disconnect()
print("🔌 Cliente desconectado.")

import paho.mqtt.client as paho
import ssl
import time

# Función cuando se establece la conexión
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado a HiveMQ Cloud.")
        client.subscribe("test/topic")  # Te puedes suscribir al topic que gustes
    else:
        print(f"Fallo en la conexión. Código: {rc}")

# Función cuando se recibe un mensaje
def on_message(client, userdata, msg):
    print(f"Mensaje recibido en '{msg.topic}': {msg.payload.decode()}")

# Crear cliente MQTT
client = paho.Client()

# Configurar credenciales
client.username_pw_set("foco_sala", "Bob22esponja")

# Configurar TLS (seguridad)
client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)

# Configurar callbacks
client.on_connect = on_connect
client.on_message = on_message

# Conexión al broker
client.connect("608359e51bfa42d5a47f3d14c8f5d47f.s1.eu.hivemq.cloud", 8883)

# Iniciar bucle
client.loop_start()

# Publicar mensaje de prueba
client.publish("test/topic", "¡Hola desde Python con TLS!", qos=1)

# Esperar para recibir respuesta
time.sleep(5)

client.loop_stop()
client.disconnect()

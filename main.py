from src.mqtt_IoT import client

def main():
    # Iniciar bucle de cliente MQTT
    client.loop_start()

    # Publicar mensaje
    client.publish("test/topic", "¡Hola desde Python con TLS!", qos=1)

    # Esperar un poco para recibir mensajes
    import time
    time.sleep(5)

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()

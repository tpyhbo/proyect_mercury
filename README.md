# Proyecto Mercury: Casa Domótica Inteligente 🏠💡

**Descripción**

Este proyecto, denominado **Mercury**, es una solución de automatización para el hogar basada en un **ESP32** con MicroPython y un broker MQTT (publicaciones/ suscripciones). Permite:

- Leer sensores de **temperatura** y **humedad** (DHT11).
- Medir **CO₂** con el sensor **MH‑Z19**.
- Publicar datos al broker MQTT.
- Suscribir un cliente Python en PC para visualizar lecturas en tiempo real.
- Controlar **4 LEDs** (2 en cocina, 2 en sala) y un **motoreductor (abanico)** vía MQTT.

---

## 🛠️ Hardware requerido

- 1x **ESP32**.
- 1x Sensor **DHT11** (temp/humedad).
- 1x Sensor **MH‑Z19** (CO₂) con adaptador UART.
- 4x LEDs (con resistencias 220 Ω).
- 1x Motoreductor amarillo (ofen conocido como "fan").
- 1x Transistor NPN (2N2222 o TIP120).
- 1x Diodo 1N4007 (flyback para el motor).
- 1x Fuente de 5 V externa (para el motor).
- Jumpers y protoboard.

---

## 📂 Estructura de archivos

```
proyect_mercury/
├── src/
│   ├── ESP32_micropython/
│   │   ├── prueba_ALL.py      # Ejemplo completo de sensores + MQTT
│   │   ├── prueba_CO2.py      # Prueba solo MH‑Z19
│   │   ├── prueba_DHT.py      # Prueba solo DHT11
│   │   └── prueba_LED.py      # Prueba de encendido LED
│   ├── mosquitto/
│   │   ├── cliente_pub_01.py  # Publicador básico
│   │   ├── cliente_pub_02.py  # Menú interactivo para control LED+fan
│   │   ├── cliente_sub_01.py  # Suscriptor simple CO₂
│   │   └── cliente_sub_02.py  # Suscriptor múltiple temp/hum/CO₂
│   └── mh_z18.py              # Librería MH‑Z19 para MicroPython
├── main.py                    # Script principal (o punto de inicio)
├── requirements.txt           # Dependencias Python (paho-mqtt)
└── README.md                  # Este archivo
```

---

## 🔌 Conexión y montaje

1. **Fuente y tierra**
   - Conecta `5V` (o `VIN`) del ESP32 a la línea +5 V de protoboard.
   - Conecta `GND` del ESP32 a la línea común de tierra.

2. **DHT11** (GPIO 4)
   - Data → Pin GPIO 4
   - VCC → 3.3 V
   - GND → Tierra

3. **MH‑Z19** (UART2)
   - TX → Pin RX2 (GPIO 16)
   - RX → Pin TX2 (GPIO 17)
   - VCC → 5 V
   - GND → Tierra

4. **LEDs** (220 Ω serie)
   - Cocina LED 1 → GPIO 15 → resistencia → ánodo → cátodo → GND
   - Cocina LED 2 → GPIO 2  → resistencia …
   - Sala   LED 1 → GPIO 4  → resistencia …
   - Sala   LED 2 → GPIO 5  → resistencia …

5. **Motoreductor (Abanico)**
   - Motor + → +5 V externo
   - Motor – → Colector de transistor
   - Emisor transistor → GND
   - Base transistor → GPIO 18 (con resistencia 1 kΩ)
   - Diodo 1N4007 en paralelo (ánodo → colector, cátodo → +5 V)

> **Tip:** puedes incluir un diagrama en `docs/diagrama.png` para facilitar el montaje.

---

## 🚀 Instalación y uso

### 1. Preparar el ESP32

- Flashea MicroPython en tu ESP32.
- Copia la carpeta `ESP32_micropython/` y `mh_z18.py` al sistema de archivos del ESP.
- Renombra tu script principal como `main.py` (por ejemplo, `prueba_ALL.py`).
- Reinicia la placa; el código iniciará automáticamente.

### 2. Instalar dependencias en PC

```bash
pip install -r requirements.txt  # Incluye paho-mqtt
```

### 3. Ejecutar cliente suscriptor

```bash
python src/mosquitto/cliente_sub_02.py
```

Verás en consola lecturas de temperatura, humedad y CO₂ en tiempo real.

### 4. Controlar LEDs y abanico

```bash
python src/mosquitto/cliente_pub_02.py
```

Sigue el menú interactivo para enviar `ON`/`OFF` a cada dispositivo.

---

## 📝 Ejemplos de topics MQTT

| Tópico             | Payload                | Descripción                  |
|--------------------|------------------------|------------------------------|
| `sensors/temp`     | `25`                   | Temperatura en °C            |
| `sensors/hum`      | `45`                   | Humedad en %                 |
| `sensors/co2`      | `CO2: 950 ppm`         | Concentración de CO₂ (ppm)   |
| `casa/cocina/led1` | `ON` / `OFF`           | Control LED Cocina 1         |
| `casa/cocina/led2` | `ON` / `OFF`           | Control LED Cocina 2         |
| `casa/sala/led1`   | `ON` / `OFF`           | Control LED Sala 1           |
| `casa/sala/led2`   | `ON` / `OFF`           | Control LED Sala 2           |
| `casa/sala/abanico`| `ON` / `OFF`           | Control Abanico (motoreductor)|

---

## 🎯 Próximos pasos

- Integrar **dashboard web** (Flask/Node-RED).
- Guardar datos históricos en **CSV** o **base de datos**.
- Implementar **alertas** (correo, Telegram) si CO₂ supera umbral.
- Añadir más sensores (luz, movimiento, etc.).

¡Gracias por usar **Proyecto Mercury**! Cualquier sugerencia, ¡haz tu pull request o abre un issue! 🚀


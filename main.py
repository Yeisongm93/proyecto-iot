import network
import urequests as requests
import ujson
import time
from machine import Pin, ADC

# ssid = "TECNO_SPARK_10_PRO"
# password = "sera_que_el"

ssid = "Soledad_restrepo"
password = "hLWap4rjNRnMYyeR52"

token_bot = "7951346270:AAGNJ8fibldxSaKOBC0QUqu4qVfh_gekrq4"
chat_id = "6656158348"
telegram_url = f"https://api.telegram.org/bot{token_bot}/sendMessage"

buzzer = Pin(15, Pin.OUT)
fire_sensor = ADC(Pin(34))
gas_sensor = ADC(Pin(33))

FIRE_THRESHOLD = 1000
GAS_THRESHOLD = 4095  

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("Conectando a WiFi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\n¡Conectado!")
    print("Dirección IP:", wlan.ifconfig()[0])

def enviar_telegram(mensaje):
    try:
        data = {
            "chat_id": chat_id,
            "text": mensaje
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(telegram_url, data=ujson.dumps(data), headers=headers)
        
        # Verificación de la respuesta
        if response.status_code == 200:
            print("Mensaje enviado:", response.text)
        else:
            print("Error al enviar mensaje, código de estado:", response.status_code)
    except Exception as e:
        print("Error al enviar mensaje:", e)

conectar_wifi()
enviar_telegram("Sistema preparado!!!")

while True:
    time.sleep(0.5)

    fire_valor = fire_sensor.read()  
    gas_valor = gas_sensor.read()  

    print("Sensor fuego:", fire_valor)
    print("Sensor gas:", gas_valor)

    if fire_valor <= FIRE_THRESHOLD:
        print("¡Fuego detectado!")
        enviar_telegram("¡ALERTA! Se ha detectado fuego")
        buzzer.on()
        time.sleep(5)
        buzzer.off()

    if gas_valor < GAS_THRESHOLD:
        print("¡Escape de gas detectado!")
        enviar_telegram("¡ALERTA! Escape de gas detectado")
        for _ in range(28):
            buzzer.on()
            time.sleep(0.1)
            buzzer.off()
            time.sleep(0.075)
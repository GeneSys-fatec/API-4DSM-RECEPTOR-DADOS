import os
import random
import time

import requests
from dotenv import load_dotenv

from sensors import create_sensor, generate_payload

load_dotenv()

config = {
    "api_url": os.getenv("API_URL"),
    "total_virtual_sensors": int(os.getenv("TOTAL_VIRTUAL_SENSORS")),
    "messages_per_burst": int(os.getenv("MESSAGES_PER_BURST")),
    "delay_between_bursts": int(os.getenv("DELAY_BETWEEN_BURSTS")),
    "delay_in_burst": float(os.getenv("DELAY_IN_BURST")),
}

print("--- Iniciando Simulador HTTP ---")

virtual_sensors = [create_sensor(i) for i in range(config["total_virtual_sensors"])]
print(f"{len(virtual_sensors)} sensores virtuais prontos.")

try:
    while True:
        print(f"\n[Burst] Enviando {config['messages_per_burst']} leituras...")

        for i in range(config["messages_per_burst"]):
            sensor = random.choice(virtual_sensors)
            payload = generate_payload(sensor)

            try:
                response = requests.post(config["api_url"], json=payload, timeout=5)

                if response.status_code == 201:
                    print(f"[OK] Dados de {payload['uid']} enviados com sucesso.")
                else:
                    print(f"[ERRO] Servidor respondeu {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"[FALHA] Não foi possível conectar à API: {e}")

            time.sleep(config["delay_in_burst"])

        print(f"--- Aguardando {config['delay_between_bursts']}s para o próximo ciclo ---")
        time.sleep(config["delay_between_bursts"])

except KeyboardInterrupt:
    print("\nSimulador encerrado.")

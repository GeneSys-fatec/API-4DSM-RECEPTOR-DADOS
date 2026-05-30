import random
import time


def create_sensor(sensor_id):
    sensor_type = random.choice(["pluviometro", "qualidade_ar", "solo"])
    return {"id": sensor_id, "type": sensor_type}


def generate_payload(sensor):
    payload = {"uid": f"{sensor['type'].upper()}-{sensor['id']}", "unixtime": int(time.time())}

    if sensor["type"] == "pluviometro":
        payload.update(
            {
                "chuva_mm": random.randint(0, 5),
                "umidade": random.randint(60, 98),
                "temperatura": round(random.uniform(18.0, 35.0), 2),
            }
        )
    elif sensor["type"] == "qualidade_ar":
        payload.update(
            {
                "co2": random.randint(300, 1000),
                "pm25": round(random.uniform(0, 50), 2),
                "qualidade_index": random.randint(1, 5),
            }
        )
    elif sensor["type"] == "solo":
        payload.update(
            {
                "umidade_solo": random.randint(10, 90),
                "ph": round(random.uniform(5.5, 7.5), 2),
                "temp_solo": round(random.uniform(15.0, 35.0), 2),
            }
        )

    return payload

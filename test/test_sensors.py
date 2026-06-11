from src.sensors import create_sensor, generate_payload


def test_create_sensor():
    sensor = create_sensor(1)
    assert "id" in sensor
    assert sensor["type"] in ["pluviometro", "qualidade_ar", "solo"]


def test_generate_payload_pluviometro():
    sensor = {"id": 1, "type": "pluviometro"}
    payload = generate_payload(sensor)
    assert "chuva_mm" in payload


def test_generate_payload_qualidade_ar():
    sensor = {"id": 2, "type": "qualidade_ar"}
    payload = generate_payload(sensor)
    assert "co2" in payload


def test_generate_payload_solo():
    sensor = {"id": 3, "type": "solo"}
    payload = generate_payload(sensor)
    assert "ph" in payload

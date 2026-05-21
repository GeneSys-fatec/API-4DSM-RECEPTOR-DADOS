from src.sensors import create_sensor, generate_payload


def test_create_sensor():
    sensor = create_sensor(1)
    assert "id" in sensor
    assert "type" in sensor
    assert sensor["type"] in ['pluviometro', 'qualidade_ar', 'solo']

def test_generate_payload_keys():
    sensor = create_sensor(99)
    payload = generate_payload(sensor)
    
    assert "uid" in payload
    assert "unixtime" in payload
    assert isinstance(payload["unixtime"], int)

def test_sensor_specific_fields():
    sensor = {"id": 1, "type": "solo"}
    payload = generate_payload(sensor)
    assert "ph" in payload
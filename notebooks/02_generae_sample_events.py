import json, random, uuid, numpy as np, pandas as pd
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from dateutil.parser import isoparse

raw_path = "/Volumes/dev/iot_fleet/raw/telemetry/"
vehicles = [f"V{i:03}" for i in range(1, 21)]

class TelemetryEvent(BaseModel):
    event_id: str
    vehicle_id: str
    driver_id: str
    event_time: str
    latitude: float = Field(..., ge=-90, le= 90)
    longitude: float = Field(..., ge=-180, le= 180)
    speed: float
    engine_temperature: float
    fuel_level: float
    battery_voltage: float
    event_type: str
    sensor_status: str

events = []

for _ in range(1000):
    event_time = datetime.now(timezone.utc) - timedelta(seconds=random.randint(0, 600))
    event = {
        "event_id": str(uuid.uuid4()),
        "vehicle_id": random.choice(vehicles),
        "driver_id": f"D{random.randint(1, 50):03d}",
        "event_time": event_time.isoformat(),
        "latitude": 33.7490 + np.random.normal(0, 0.05),
        "longitude": -84.3880 + np.random.normal(0, 0.05),
        "speed": round(max(0, np.random.normal(45, 20)), 2),
        "engine_temperature": round(np.random.normal(90, 15), 2),
        "fuel_level": round(random.uniform(5, 100), 2),
        "battery_voltage": round(np.random.normal(12.5, 0.7), 2),
        "event_type": "telemetry",
        "sensor_status": random.choice(["OK", "OK", "OK", "WARN", "FAIL"])
    }

    validated = TelemetryEvent(**event)
    events.append(validated.model_dump())

events_df = pd.DataFrame(events)

output_file_path = raw_path + "events_001.json"
dbutils.fs.put(output_file_path, "\n".join(json.dumps(e) for e in events), overwrite=True)

display(dbutils.fs.ls(raw_path))
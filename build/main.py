import hyundai_kia_connect_api as api
import json
import os
import prometheus_client  as prometheus
import time

battery_percentage = prometheus.Gauge(
  name='vehicle_battery_percentage', 
  documentation='Percentage of battery remaining',
  labelnames=['vehicle_id']
)

if __name__ == '__main__':
  manager = api.VehicleManager(
    region=int(os.getenv('API_REGION', '3')),
    brand=int(os.getenv('API_BRAND', '1')),
    username=os.getenv('API_USERNAME'),
    password=os.getenv('API_PASSWORD'),
    pin=os.getenv('API_PIN', '')
  )
  prometheus.start_http_server(8000)

  while True:
    try:
      manager.check_and_refresh_token()
      manager.update_all_vehicles_with_cached_state()
    except Exception as exc:
      print(f'Exception occurred: {exc}')
      next
    for id, vehicle in manager.vehicles.items():
      battery_percentage.labels(vehicle_id=id).set(vehicle.car_battery_percentage)
      print(json.dumps({
        'id': id,
        'name': vehicle.name,
        'battery_percentage': vehicle.car_battery_percentage,
        'last_updated': vehicle._last_updated_at.isoformat()
      }))
    time.sleep(int(os.getenv('API_POLLING_INTERVAL', '900')))
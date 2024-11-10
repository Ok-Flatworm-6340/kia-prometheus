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
door_lock_status = prometheus.Gauge(
  name='vehicle_door_lock_status',
  documentation='Indicates whether the doors are locked',
  labelnames=['vehicle_id']
)
engine_running_status = prometheus.Gauge(
  name='vehicle_engine_running_status',
  documentation='Indicates whether the engine is running',
  labelnames=['vehicle_id']
)
fuel_level = prometheus.Gauge(
  name='vehicle_fuel_level',
  documentation='Percentage of fuel remaining',
  labelnames=['vehicle_id']
)
info = prometheus.Info(
  name='vehicle',
  documentation='Vehicle information',
  labelnames=['vehicle_id']
)
odometer = prometheus.Gauge(
  name='vehicle_odometer',
  documentation='Vehicle odometer value',
  labelnames=['vehicle_id', 'unit']
)
smart_key_status = prometheus.Gauge(
  name='vehicle_smart_key_warning_status',
  documentation='Indicates the smart key battery is low',
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
      door_lock_status.labels(vehicle_id=id).set((0,1)[vehicle.is_locked])
      engine_running_status.labels(vehicle_id=id).set((0,1)[vehicle.engine_is_running])
      fuel_level.labels(vehicle_id=id).set(vehicle.fuel_level)
      info.labels(vehicle_id=id).info({
        'vehicle_color': vehicle.data['vehicleConfig']['vehicleDetail']['vehicle']['exteriorColor'],
        'vehicle_model': vehicle.model,
        'vehicle_name': vehicle.name,
        'vehicle_trim': vehicle.data['vehicleConfig']['vehicleDetail']['vehicle']['trim']['trimName'],
        'vehicle_vin': vehicle.data['vehicleConfig']['vehicleDetail']['vehicle']['vin'],
        'vehicle_year': vehicle.data['vehicleConfig']['vehicleDetail']['vehicle']['trim']['modelYear'],
      })
      odometer.labels(vehicle_id=id, unit=vehicle.odometer_unit).set(vehicle.odometer)
      smart_key_status.labels(vehicle_id=id).set((0,1)[vehicle.smart_key_battery_warning_is_on])
      print(json.dumps({
        'id': id,
        'doors_locked': vehicle.is_locked,
        'engine_running': vehicle.engine_is_running,
        'fuel_level': vehicle.fuel_level,
        'name': vehicle.name,
        'odometer': vehicle.odometer,
        'battery_percentage': vehicle.car_battery_percentage,
        'last_updated': vehicle._last_updated_at.isoformat()
      }))
    time.sleep(int(os.getenv('API_POLLING_INTERVAL', '900')))
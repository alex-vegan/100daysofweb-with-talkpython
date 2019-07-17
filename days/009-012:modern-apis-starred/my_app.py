from apistar import App, Route, types, validators, http
import json
from datetime import date, datetime
from typing import List

# help function before DB using

def _load_data_to_dict():
    with open('MY_MOCK_DATA.json') as f:
        devices = json.loads(f.read())
        for device in devices:
            _string_date = device['start_date']
            _datetime = datetime.strptime(_string_date, '%m/%d/%Y')
            device['start_date'] = _datetime.date()
        return {device['id']:device for device in devices}

devices = _load_data_to_dict()

DEVICE_MODELS = set([device['device_model'] for device in devices.values()])

_default_date = datetime.strptime('1/1/2010', '%m/%d/%Y')  
DEFAULT_DATE = _default_date.date()


#breakpoint()

# create Class with API Star validators

class Device(types.Type):
    id = validators.Integer(allow_null=True, minimum=1, maximum=999)
    device_model = validators.String(enum=list(DEVICE_MODELS))
    ip_address = validators.String(default='127.0.0.1')
    remote_access_type = validators.String(enum=['ssh','telnet','http','https'], default='ssh')
    login = validators.String(default='cisco')
    password = validators.String(default='cisco', min_length=5)
    secret = validators.String(default='cisco', min_length=5)
    apc = validators.Boolean(default=False)
    free_access_to_site = validators.Boolean(default=True)
    start_date = validators.Date(default=DEFAULT_DATE)
    company_name = validators.String(allow_null=True)
    city = validators.String(allow_null=True)
    city_address = validators.String(allow_null=True)
    owner = validators.String(allow_null=True)
    phone = validators.String(min_length=12, max_length=12)
    email = validators.String(allow_null=True)



# CRUD functions

def read_all_devices() -> List[Device]:
    return [Device(device[1]) for device in sorted(devices.items())] 


def create_new_device(device: Device) -> http.JSONResponse:
    device_id = max(devices.keys()) + 1
    device.id = device_id
    devices[device_id] = device
    return http.JSONResponse(Device(device), status_code=201)


def read_device(device_id: int) -> http.JSONResponse:
    if not devices.get(device_id):
        return http.JSONResponse({'error': 'no device'}, status_code=404)
    return http.JSONResponse(Device(device), status_code=200)


def update_device(device_id: int, device: Device) -> http.JSONResponse:
    if not devices.get(device_id):
        return http.JSONResponse({'error': 'no device'}, status_code=404)
    device.id = device_id
    return http.JSONResponse(Device(device), status_code=200)


def delete_device(device_id: int) -> http.JSONResponse:
    if not devices.get(device_id):
        return http.JSONResponse({'error': 'no device'}, status_code=404)
    del devices[device_id]
    return http.JSONResponse({}, status_code=204)


# CRUD routes

routes = [
    Route('/', method='GET', handler=read_all_devices),
    Route('/', method='POST', handler=create_new_device),
    Route('/{device_id}/', method='GET', handler=read_device),
    Route('/{device_id}/', method='PUT', handler=update_device),
    Route('/{device_id}/', method='DELETE', handler=delete_device),
]

# create application

my_app = App(routes=routes)

if __name__ == '__main__':    
    my_app.serve('127.0.0.1', 5050, debug=True)

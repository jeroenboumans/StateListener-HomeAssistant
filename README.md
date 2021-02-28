# State Listener for Home Assistant (and Pimoroni)

![](https://i.ibb.co/ZKhKqqH/Schermafbeelding-2021-02-28-om-09-21-47.png)

This is a collection of Python script to log state changes provided by the Home Asssistent websocket API. Each script contains of two parallel processes:
- Logger: when desired states received data from Home Assistant's socket the logger starts outputting these.
- Listener: the handler to listen and write states changes to memory which will be picked up by the logger.

## Requirements

* An environment able to run python(3) scripts.
* Optional: For the `sensor_ws_phat.py` you'll need a [Micro Dot pHAT](https://shop.pimoroni.com/products/microdot-phat?variant=25454635527) on a Raspberry Pi (zero).

## Installation

Install the script on your environment and make sure you've noted you're Home Assistant profile and configuration details:
Specify these in the script you're about to run:

```bash
# check {host}}:{port}/profile to generate an Auth token
token = HASS_IO_AUTHORIZATION_TOKEN
port = HASS_IO_PORT
host = HASS_IO_HOSTNAME_OR_URL
```

Provide the states the listener should listen to. These will be added to the logger output.

```python
entities = [
    "sensor.power_tariff",
    "sensor.power_consumption_watt",
    "sensor.gas_consumption",
    ...
]
```

Install the dependencies if not already on your environment:

```bash
$ pip install asyncio && pip3 install asyncws
```

Optional: in case of using the Micro Dot pHAT, install their library as well:

```bash
$ curl https://get.pimoroni.com/microdotphat | bash
```

## Usage

### Run logger

```bash
# Run logger or pHAT logger 
$ python3 log.py
$ python3 log.phat.py

# Output Logger
Start logger...
Start socket...
writing sensor.power_tariff to cache
writing sensor.gas_consumption to cache
writing sensor.power_consumption_watt to cache
low
6692.597 m3
372 W
```

### Run logger after boot
Add a startup cronjob to the crontab of your system
```bash
# Open de crontab file
$ crontab -e

# Add to bottom:
@reboot sleep 30 && python3 /home/pi/log.phat.py & 2>&1 >> /home/pi/log.phat.log
```

## Contributing
Suggestions are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

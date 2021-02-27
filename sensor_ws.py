#!/usr/bin/env python

# pip install asyncio
# pip3 install asyncws

import time
from microdotphat import write_string, set_decimal, clear, show
import asyncws
import asyncio
import threading
import json

token = "YOUR_HASS_IO_TOKEN"
host = "YOUR_HOST_OR_URL"
port = 8123
cache = {} # cache
entities = [
    "sensor.power_tariff",
    "sensor.power_consumption_watt",
    "sensor.gas_consumption"
]
    
async def initLogger():
    print("Start logger...")

    await asyncio.sleep(1) 
    
    while True:    
        if len(cache) == 0:
            await asyncio.sleep(2) 
            
        else:
            try:
                for key in cache:
                    print(cache[key])
                    
                    # Write to PHAT
                    clear()
                    write_string(cache[key], kerning=False)
                    show()
                    await asyncio.sleep(2) 
                
            except Exception:
               pass
        
async def initSocket():
    websocket = await asyncws.connect('ws://{}:{}/api/websocket'.format(host, port))

    await websocket.send(json.dumps({'type': 'auth','access_token': token}))
    await websocket.send(json.dumps({'id': 1, 'type': 'subscribe_events', 'event_type': 'state_changed'}))
    
    print("Start socket...")

    while True:
        message = await websocket.recv()
        if message is None:
            break
        
        try:   
            data = json.loads(message)['event']['data']
            entity_id = data['entity_id']
            
            if entity_id in entities:
                
                print("writing {} to cache".format(entity_id))
                
                if 'unit_of_measurement' in data['new_state']['attributes']:
                    cache[entity_id] = "{} {}".format(data['new_state']['state'], data['new_state']['attributes']['unit_of_measurement'])
                else:
                    cache[entity_id] = data['new_state']['state']
                    
        except Exception:
            pass

async def main(): 
    listen = asyncio.create_task(initSocket()) 
    log = asyncio.create_task(initLogger()) 
    await listen
    await log

if __name__ == "__main__":    
    asyncio.run(main())

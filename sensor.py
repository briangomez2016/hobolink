"""Platform for sensor integration."""
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from requests import Session
import datetime
import json

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([ExampleSensor(config['nombre'],config['serial'])])


class ExampleSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self,nombre,serial):
        """Initialize the sensor."""
        self.nombre = nombre
        self.serial = serial
        self._state = None
        self.unit = None
    @property
    def name(self):
        """Return the name of the sensor."""        
        return self.nombre

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._state == None:
            return "Cargando..."
        return "{:.2f}".format(float(self._state))

    @property
    def unit_of_measurement(self):
        if self._state == None:
            return "" 
        else:
            return self.unit


    def update(self):
        x = datetime.datetime.now()
        #x = x + datetime.timedelta(hours=3)
        #print(x)     
        fecha_actual = "%s-%02d-%02d %02d:%02d:%02d" % (x.year,x.month,x.day,x.hour, x.minute, x.second ) 
        #print(fecha_actual)
        x = x - datetime.timedelta(minutes=40)   
        fecha_anterior = "%s-%02d-%02d %02d:%02d:%02d" % (x.year,x.month,x.day,x.hour, x.minute, x.second ) 
        #print(fecha_anterior)
        url = "https://webservice.hobolink.com/restv2/data/json"

        payload = "{\n  \"action\": \"\",\n  \"authentication\": {\n    \"password\": \"dlVpjPGQ\",\n    \"token\": \"a31f06b4fd6efa191a5d3dd19658cf337fe2854b\",\n    \"user\": \"lapostergada\"\n  },\n  \"query\": {\n    \"end_date_time\": \""+fecha_actual+"\",\n    \"loggers\": [20925436],\n    \"start_date_time\":  \""+fecha_anterior+"\"\n  }\n}\n"
        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',     
        }
        response = requests.request("POST", url, headers=headers, data = payload)
        if(response.ok):
            to_python = json.loads(response.text.encode('utf8'))
            to_python = to_python['observationList'][::-1]
            for x in to_python:
                if(x["sensor_sn"]== self.serial):
                    self._state =x["si_value"]
                    self.unit = x["si_unit"]
                    break



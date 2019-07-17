import artikcloud
from artikcloud.rest import ApiException
import sys, getopt
import time, random, json
from pprint import pprint
import Adafruit_DHT


def main(argv):
    sensor = Adafruit_DHT.DHT22
    pin = 4

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    DEFAULT_CONFIG_PATH = 'config.json'

    with open(DEFAULT_CONFIG_PATH, 'r') as config_file:
            config = json.load(config_file)
    print(config)

    artikcloud.configuration = artikcloud.Configuration();
    artikcloud.configuration.access_token = config['device_token']

    api_instance = artikcloud.MessagesApi()

    device_message = {}

    if humidity is not None and temperature is not None:
        try:
            device_message['temp'] = temperature
            device_message['humidity'] = humidity
            device_sdid = config['device_id']
            ts = None
            data = artikcloud.Message(device_message, device_sdid, ts) 

            # Debug Print oauth settings
            pprint(artikcloud.configuration.auth_settings())

            # Send Message
            api_response = api_instance.send_message(data)
            pprint(api_response)
        except ApiException as e:
            pprint("Exception when calling MessagesApi->send_message: %s\n" % e)
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])

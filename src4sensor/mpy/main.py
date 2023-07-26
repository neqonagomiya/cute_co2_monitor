import machine
import time
import network
import umqtt.simple

from configf.config import Config
from sensor.co2_sensor import SCD4X

def gen_json(val):
    msg = '{"data":' + str(val) + ',"write": true}'
    return msg

# configs
config        = Config()
MY_ID         = config.get("my_id")
BROKER_URL    = config.get("broker_URL")
BROKER_PORT   = config.get("broker_port")
USER_ID       = config.get("user_id")
CHANNEL       = config.get("channel")
RESOURCE_CO2  = config.get("resource_co2")
RESOURCE_temp = config.get("resource_temp")
RESOURCE_humi = config.get("resource_humi")
PUBLISH_FLAG  = config.get("publish_flag")
PUBLISH_DUR   = config.get("publish_duration")

if PUBLISH_FLAG == "True":
    publish_flag = True
else:
    publish_flag = False
publish_duration = int(PUBLISH_DUR) # sec
topic_co2 = CHANNEL + "/" + RESOURCE_CO2
topic_temp = CHANNEL + "/" + RESOURCE_temp
topic_humi = CHANNEL + "/" + RESOURCE_humi
topics = [topic_co2, topic_temp, topic_humi]

# setting network
lan = network.LAN()
lan.active(True)
while not lan.isconnected():
    time.sleep(1)
print("lan_config:", lan.ifconfig())

# setting MQTT
# [](https://mpython.readthedocs.io/en/master/library/mPython/umqtt.simple.html)
# MQTTClient(client_id, server, port=0, user=None,
# password=None, keepalive=0, ssl=False, ssl_params{})
client= umqtt.simple.MQTTClient(
    MY_ID,
    BROKER_URL,
    port=int(BROKER_PORT),
    user=USER_ID,
    password="",
    keepalive=60
)

client.connect()


# init co2 sensor
i2c = machine.I2C(1)
scd4x = SCD4X(i2c)
scd4x.start_periodic_measurement()


# main loop
while True:
    co2_ppm = scd4x.co2
    temp_deg = scd4x.temp
    humi_per = scd4x.humi
    msg_co2 = gen_json(co2_ppm)
    msg_temp = gen_json(temp_deg)
    msg_humi = gen_json(humi_per)
    msg = [msg_co2, msg_temp, msg_humi]

    if publish_flag == True:
        # publish co2, temp, humi
        for i in range(len(topics)):
            client.publish(topics[i], msg[i])
            print("Publish:" + topics[i] + " " + msg[i])
    else:
        print("publish_flag is False")
    time.sleep(publish_duration) # sec

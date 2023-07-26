import requests
import json
import numpy as np
import time
from sensor import Srv_sens

# 自然の屋外雰囲気の二酸化炭素濃度レベルは、400ppm程度
# 約1,000ppmで２０%程度の人が不快感、眠気を感じ、
# 2000ppmでは大部分の人が不快感、頭痛、めまいや吐き気を発症します。
# [https://www.michell-japan.co.jp/blog/blog3_appnote_rot21-01/]()
"""
 "POST " I483_NAPKIN_PATH " HTTP/1.1\r\n"
        "Host: " I483_NAPKIN_HOST "\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n\r\n%s",
        strlen(payload),
"""

"""
curl -i -X GET \ 
     -H "Content-Type: application/json" \
     -H "napkin-account-api-key: ''" jaistneqo.npkn.net/environment-store/2310063

curl -i -X DELETE -H "Content-Type: application/json" -H "napkin-account-api-key: ''" jaistneqo.npkn.net/environment-store/2310063

     
"""


DEVICE_ID = 2310063
# max_co2 = 1000
# min_co2 = 400
max_co2 = 2000
min_co2 = 950
# max_co2 = 2500
# min_co2 = 2000
max_temp=30
min_temp=20
max_humi=60
min_humi=40
duration=60 # sec

co2_sens = Srv_sens(max_val=max_co2, min_val=min_co2)
humi_sens = Srv_sens(max_val=max_humi, min_val=min_humi)
temp_sens = Srv_sens(max_val=max_temp, min_val=min_temp)

HTTP = "https://"
HOST = "jaistneqo.npkn.net"
PATH = "/environment-store/"
PORT = 80
API_KEY = "7ca8c415d2954130ab38eda493af97ad"

#STUDENT_ID = 2310063
#BMP180_ID = 0
#SCD41_ID = 1
URL = HTTP + HOST + PATH + str(DEVICE_ID)
print(URL)

headers = {
            "content-type": "application/json",
            "napkin-account-api-key": API_KEY
           } 


while True:
    try:
        co2_data = co2_sens.read_sens()
        humi_data = humi_sens.read_sens()
        temp_data = temp_sens.read_sens()
        print("co2:{}, humi:{}, temp:{} ".format(co2_data, humi_data, temp_data))

        #body = {"student_id": STUDENT_ID, "bmp180_id": BMP180_ID, "scd41_id": SCD41_ID}
        body = {
            "CO2": co2_data,
            "Humidity": humi_data,
            "Temperature": temp_data
            }
        
        response = requests.post(URL, 
                                 data=json.dumps(body), 
                                 headers=headers)
        print(response)
        time.sleep(duration)

    except KeyboardInterrupt:
        print("fin.")
        break




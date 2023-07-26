from napkin import request, response, store
import time
import datetime
import sys
import json
import pygal
import statistics
import numpy as np

"""
https://jaistneqo.npkn.net/environment-stat/{device_id}/{ways}/{periods}/{data_type}

"""

def chart(data, title=""):
    chart = pygal.DateTimeLine(style=pygal.style.RotateStyle('#18afa7'), x_label_rotation=80)
    chart.title = title
    chart.add(title, data)
    return chart.render(
        is_unicode=True, disable_xml_declaration=True)

def timestamp2JST(time_stamp):
    timeJST = (datetime.datetime.fromtimestamp(time_stamp) + datetime.timedelta(hours=9)).replace(microsecond=0)
    return timeJST

def pick_data(p, x, select_data="CO2"):
    m = -p-1
    calc_list = []   
    for i in range(len(x["data"][m:-1])):
        calc_list.append(x["data"][m:-1][i][select_data]) 
    return calc_list


# Make a request to the endpoint and replace {name} with your name.
# https://docs.napkin.io/guides/http-requests Path Parameters
# https://jaistneqo.npkn.net/environment-stat/{device_id}/{ways}/{periods}/{data_type}

device_id = request.path_params["device_id"]
ways = request.path_params["ways"]
periods = request.path_params["periods"]
data_type = request.path_params["data_type"]

"""
ways domain
    - periods domain

- [] all
    - [x] all
    - [x] latest30 min
    - [x] 1h
- []max/min
    - [x] letest30 min
    - [x] 1h
- []mean/var
    - [x] l30m
    - [x] 1h

data_type
- CO2
- Temperature
- Humidity
"""

# User side endpoint 
if request.method == "GET":
    if store.has(device_id):
        if ways=="all":
            """
            serv all data
            """
            data = store.get(device_id)
            if periods=="all":
                data4serv = [
                    #(datetime.datetime.fromtimestamp(x["_t"]).strftime("%Y-%m-%dT%H:%M:%S"), x["Temperature"]) for x in data["data"]
                    #((datetime.datetime.fromtimestamp(x["_t"])+datetime.timedelta(hours=9)).replace(microsecond=0), x["Temperature"]) for x in data["data"]
                    (timestamp2JST(x["_t"]), x[data_type]) for x in data["data"]
                    #(datetime.datetime.fromtimestamp(x["_t"]), x["Temperature"]) for x in data["data"]
                ]
            elif periods=="l30m":
                data4serv = [
                    (timestamp2JST(x["_t"]), x[data_type]) for x in data["data"][-31:-1]
                ]
            elif periods=="1h":
                data4serv = [
                    (timestamp2JST(x["_t"]), x[data_type]) for x in data["data"][-61:-1]
                ]
            else:
                response.headers = {"Content-Type": "application/json"}
                response.status_code = 404
                response.body = {"status": "not found"}
            #print(data4serv)
            response.headers = {"Content-Type": "text/html"}
            response.status_code = 200
            response.body = chart(
                data4serv,
                title=data_type,
            )


        elif ways=="minmax":
            data = store.get(device_id)
            if periods=="l30m":
                data_list = pick_data(30, data, select_data=data_type)
            elif periods=="1h":
                data_list = pick_data(60, data, select_data=data_type)
            else:
                response.headers = {"Content-Type": "application/json"}
                response.status_code = 404
                response.body = {"status": "not found"}

            mini_val = np.min(data_list)
            max_val = np.max(data_list)
            response.headers = {"Content-Type": "application/json"}
            response.status_code = 200
            json_dict = json.dumps({"min": mini_val, "var": max_val})
            response.body = json_dict


        elif ways=="mean":
            data = store.get(device_id)
            if periods=="l30m":
                data_list = pick_data(30, data, select_data=data_type)
            elif periods=="1h":
                data_list = pick_data(60, data, select_data=data_type)
            else:
                response.headers = {"Content-Type": "application/json"}
                response.status_code = 404
                response.body = {"status": "not found"}
            
            mean = np.mean(data_list)
            var = np.var(data_list)
            response.headers = {"Content-Type": "application/json"}
            response.status_code = 200
            json_dict = json.dumps({"mean": mean, "var": var})
            response.body = json_dict
        
        else:
            response.headers = {"Content-Type": "application/json"}
            response.status_code = 404
            response.body = {"status": "not found"}
else:
    response.headers = {"Content-Type": "text/plain"}
    response.status_code = 405
    response.body = "HTTP METHOD NOT ALLOWED"
from napkin import request, response, store
import time

# https://docs.napkin.io/guides/http-requests Path Parameters
device_id = request.path_params["device_id"]

# Device side endpoint
if request.method == "GET":
    if store.has(device_id):
        response.headers = {"Content-Type": "application/json"}
        response.status_code = 200
        response.body = store.get(device_id)
    else:
        response.headers = {"Content-Type": "application/json"}
        response.status_code = 404
        response.body = {"status": "not found"}

elif request.method == "POST" and request.is_json:
    data_to_be_appended = request.body
    data_to_be_appended["_t"] = time.time()
    #data_to_be_appended["_t"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    history = store.get(device_id)["data"] or []
    history += [data_to_be_appended]
    store.put(device_id, history)
    response.headers = {"Content-Type": "application/json"}
    response.status_code = 200
    response.body = {"status": "ok"}

elif request.method == "DELETE":
    store.put(device_id, [])
    response.headers = {"Content-Type": "application/json"}
    response.status_code = 200
    response.body = {"status": "ok"}
else:
    response.headers = {"Content-Type": "text/plain"}
    response.status_code = 405
    response.body = "HTTP METHOD NOT ALLOWED"

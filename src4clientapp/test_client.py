import tomli
from client import Client

# setting
with open("./setting/setting.toml", "rb") as f:
    tomlist = tomli.load(f)

HTTP = "https://"
HOST = tomlist["napkin"]["HOST"]
PATH = tomlist["napkin"]["PATH"]
ways = tomlist["napkin"]["ways"]
periods = tomlist["napkin"]["periods"]
data_type = tomlist["napkin"]["data_type"] #"Humidity", "Temperature"
PORT = tomlist["napkin"]["PORT"]
API_KEY = tomlist["napkin"]["API_KEY"]
DEVICE_ID = tomlist["napkin"]["DEVICE_ID"]

napkin_client = Client(HTTP, HOST, PATH, ways, periods,
                       data_type, PORT, API_KEY, DEVICE_ID)
mean_val = napkin_client.get_mean()

print(mean_val)

if mean_val>=0 and mean_val<1000:
    print("level 1")
elif mean_val>=1000 and mean_val<2000:
    print("level 2")
else:
    print("level 3")
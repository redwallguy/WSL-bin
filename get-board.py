import json
import requests
import sys

board = sys.argv[1] #for board-specific downloading

token = ""
next = None
rate_limit = 0
with open("env.json") as f:
    env_dict = json.load(f)
    token = env_dict["PINTEREST_API_TOKEN"]
    next = env_dict["PINTEREST_NEXT_URL"]
    rate_limit = env_dict["PINTEREST_RATE_LIMIT_REMAINING"]

if rate_limit != 0:
    if next is not None:
        r = requests.get(next)
    else:
        r = requests.get("https://api.pinterest.com/v1/boards/devmoney/"+board+"/pins",params={
            "fields": "id,url,image", "limit": 100, "access_token": token
        })
    with open("env.json", "r") as f:
        env_dict = json.load(f) 
    env_dict["PINTEREST_NEXT_URL"] = r.json()["page"]["next"]
    env_dict["PINTEREST_RATE_LIMIT_REMAINING"] = r.headers["X-Ratelimit-Remaining"]
    with open("env.json", "w") as f:
        json.dump(env_dict,f)
    jresp = r.json()
    for pin in jresp["data"]:
        with open(str(pin["id"])+".jpg", "wb") as f:
            try:
                f.write(requests.get(pin["image"]["original"]["url"]).content)
            except Exception as e:
                print(e)
    print(jresp)
    print(r.headers)
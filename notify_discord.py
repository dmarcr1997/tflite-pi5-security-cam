import requests
import json
def send_image_to_discord(image_path, message="Intruder!"):
    with open("config.json") as config_file:
        config = json.load(config_file)
    
    webhook_url = config["webhook_url"]
    with open(image_path, "rb") as img:
        files = {"file": img}
        data = {"content": message}

        response = requests.post(webhook_url, data=data, files=files)
    return response.status_code == 204
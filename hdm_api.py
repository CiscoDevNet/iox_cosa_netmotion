import requests
import config as config
import json

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def show_cmd(cmd):

    url = config.cfg.get("hdm_api_info", "url")
    token = config.cfg.get("hdm_api_info", "auth_token")

    payload = cmd
    headers = {"Authorization": token, "Content-Type": "text/plain"}

    response = requests.post(url, data=payload, headers=headers, verify=False)

    resp_text = response.text

    # print(resp_text)

    resp_data = json.loads(resp_text)

    cmd_out = resp_data["output"]

    return cmd_out

# print(show_cmd("show ver | include Version"))

# MIT License

# Copyright (c) 2020 Sandeep Bhat

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Monitor your IP address and post slack on change."""

import json
from datetime import datetime
import requests
import netifaces

IPINFO_FILEPATH = "/home/user/.ipinformation"
ALLOWLIST = ["mynetiface1", "mynetiface2", "mynetiface3"]
ERROR_FILEPATH = "/home/user/.ipinformation.error"
SLACK_WEBHOOK = "https://hooks.slack.com/services/XXXXXXXXX/YYYYYYYYY/6c7e4003b173e3d0c062e850"


def get_ip_information():
    """Get IP addresses for interfaces in ALLOWLIST."""
    ipinfo = dict()
    ifaces = netifaces.interfaces()

    for iface in ifaces:
        if iface in ALLOWLIST:
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                ipinfo[iface] = addrs[netifaces.AF_INET][0]["addr"]

    return ipinfo


def post_to_slack(ipinfo: dict):
    """Post message to slack using webhooks."""
    headers = {"Content-type": "application/json"}
    data = {"text": json.dumps(ipinfo)}
    response = requests.post(url=SLACK_WEBHOOK, data=json.dumps(data), headers=headers)
    if not response.ok:
        with open(ERROR_FILEPATH, "a") as errfile:
            errfile.write("{}: Posting message to slack failed: {}".format(
                datetime.timestamp(datetime.now()), response))


def has_ip_address_changed(ipinfo: dict):
    """Check if IP addresses have changed."""
    last_ipinfo = dict()

    try:
        with open(IPINFO_FILEPATH, "r") as ipinfo_file:
            last_ipinfo = json.load(ipinfo_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return True

    if ipinfo != last_ipinfo:
        return True

    return False


def save_ip_information(ipinfo: dict):
    """Save current IP address information to disk."""
    with open(IPINFO_FILEPATH, "w") as ipinfo_file:
        json.dump(ipinfo, ipinfo_file, indent=4)


if __name__ == "__main__":
    ip_info = get_ip_information()
    if has_ip_address_changed(ip_info):
        save_ip_information(ip_info)
        post_to_slack(ip_info)

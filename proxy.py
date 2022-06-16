import requests
from outline_api import (
    Manager,
    get_key_numbers, 
    get_active_keys)
from outline_vpn.outline_vpn import OutlineVPN

# Setup the access with the API URL (Use the one provided to you after the server setup)
proxy = OutlineVPN(api_url="https://127.0.0.1:51083/xlUG4F5BBft4rSrIvDSWuw")
url = "https://httpbin.org/ip"

re = requests.get(url, proxies=proxy)

print(re.json())

# apiurl = "http://127.0.0.1/apikey"
# apicrt = "apicert"
# manager = Manager(apiurl=apiurl, apicrt=apicrt)

# new_key = manager.new()
# if new_key is not None:
#     print(new_key)

# keys = get_key_numbers("127.0.0.1", "999")
# print(keys)

# active_keys = get_active_keys("127.0.0.1", "999")
# print(active_keys)

# url = "https://httpbin.org/ip"

# proxy = { "https://": "Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpoZzQ5JFdIODk0M2cz@ak1225.free.www.outline.network:18760/" }

# re = requests.get(url, proxies=proxy)

# print(re.json())
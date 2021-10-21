from typing import Optional, Any, List, Mapping
import requests
import dataclasses
from .storage import JSONConfig
from .auth import Auth, DeviceInfo, register_device_with_token
from .signer import Signer
from .api import STKClient, upload_file
import json


def main():
    s = JSONConfig("storage.json", "")
    if s.get("access_token") is None:
        auth = Auth()
        url = auth.get_url()
        print(url)
        redirect_url = input("Enter redirect url: ")
        s["access_token"] = auth.handle_redirect_url(redirect_url)
    print(s["access_token"])
    if s.get("device_info") is None:
        device_info = register_device_with_token(s["access_token"])
        s["device_info"] = dataclasses.asdict(device_info)
    device_info = DeviceInfo.from_dict(s["device_info"])
    print(device_info)
    c = STKClient(Signer.from_device_info(device_info))
    print(c.get_list_of_owned_devices())

if __name__ == "__main__":
    main()

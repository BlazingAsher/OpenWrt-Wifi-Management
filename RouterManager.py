import requests
import time

class RouterManager:
    def __init__(self, scheme, host):
        self._s = requests.Session()
        self._s.verify = False
        self.lastAuth = 0
        self._url = scheme + "://" + host
        
    def authenticate(self, username, password):
        self._s.post(self._url + '/cgi-bin/luci/rpc/auth', json={
                "id": 1,
                "method": "login",
                "params": [
                    username,
                    password
                    ]
            })
        self.lastAuth = time.time()
        
    def getWirelessConfig(self):
        return self._s.post(self._url + '/cgi-bin/luci/rpc/uci', json={
                "id": 1,
                "method": "get_all",
                "params": [
                    "wireless"
                    ]
            }).json()

    def getNetworkState(self, cfg):
        state = self._s.post(self._url + '/cgi-bin/luci/rpc/uci', json={
                "id": 1,
                "method": "get_state",
                "params": [
                    "wireless",
                    cfg,
                    "disabled"
                    ]
            }).json()["result"]
        return True if state or state is None else False

    def disableNetwork(self, cfg):
        return self._s.post(self._url + '/cgi-bin/luci/rpc/uci', json={
                "id": 1,
                "method": "set",
                "params": [
                    "wireless",
                    cfg,
                    "disabled",
                    '1'
                    ]
            }).json()

    def enableNetwork(self, cfg):
        return self._s.post(self._url + '/cgi-bin/luci/rpc/uci', json={
                "id": 1,
                "method": "delete",
                "params": [
                    "wireless",
                    cfg,
                    "disabled"
                    ]
            }).json()

    def commitSettings(self):
        return self._s.post(self._url + '/cgi-bin/luci/rpc/uci', json={
                "id": 1,
                "method": "commit",
                "params": [
                    "wireless",
                    ]
            }).json()

    def reloadWifi(self):
        return self._s.post(self._url + '/cgi-bin/luci/rpc/sys', json={
                "id": 1,
                "method": "call",
                "params": [
                    "/sbin/wifi reload"
                    ]
            }).json()

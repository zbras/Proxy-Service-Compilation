from proxy import Proxy
import regex as re
import requests as req

class ProxyService():
    #   Factory class for various API supported proxy list services.
    #   Supports writing successfully connected proxies to a text file for storage.
    #   Supports multiple different API response formats, as outlined and processed in the format_proxy_request method.
    #   New response formats must be added in this method, as well as the child class by specifying a new 'resolve_type' attribute and processing logic.
    #   TODO: Reformat connection file as dictionary, eg: {"x.x.x.x": {"port": "x", "last_connected": datetime.datetime}}

    def __init__(self, web_address, resolve_type, name):

        self.name = name
        self.addr = web_address
        self.resp = resolve_type
        self.connections = set()

        print(f'////////////////\tTESTING {self.name}')

        self.retrieve_proxies()

        #   If response code from the API request is not 200, we gracefully exit without further processing.
        if self.check_status():
            self.read_from_proxy_file()
            self.format_proxy_request()
            self.connect_to_proxy_list()
            self.add_to_proxy_file()

    def retrieve_proxies(self) -> None:
        #   Poll API for proxies.
        self.proxies = req.get(self.addr)

    def check_status(self) -> bool:
        #   Returns True on API query success, and False on failure.
        if self.proxies.status_code != 200:
            print(f'Error: Server returned {self.proxies.status_code}')
            return False

        return True

    def format_proxy_request(self) -> None:
        #   Logic for processing different API response types into the format {"x.x.x.x": "x", ...}.
        #   If adding a new subclass to extend the API functionality, the logic in this method must be updated to reflect conversion from the new response type.
        temp_proxies = {}

        #   Logic 01 - Data is in the format of json:
        #       {"data": [{"ip": "x.x.x.x", "port": "x"}]}
        if self.resp == 'data/json':
            self.proxies = self.proxies.json()
            for proxy in self.proxies['data']:
                temp_proxies[proxy['ip']] = proxy['port']

        #   Logic 02 - Data is in the format of text:
        #       x.x.x.x:x
        #       x.x.x.x:x ...
        elif self.resp == 'text':
            self.proxies = self.proxies.text
            for match in re.findall('((\d{1,3}.){3}(\d{1,3}))(?:\:)(?=(\d{1,6}))', self.proxies):
                temp_proxies[match[0]] = match[3]

        else:
            print(f'No method for processing API data of type {self.resp}!')
            quit()

        self.proxies = temp_proxies

    def connect_to_proxy_list(self) -> None:
        #   After the API response has been processed, loop through all the proxies and attempt to connect to them, storing successful connections in self.connections to be added to a text file for storage.
        for proxy in self.proxies:
            prox = Proxy(proxy, self.proxies[proxy])

            if prox.check_service():
                self.connections.add(f'{proxy}:{self.proxies[proxy]}')

    def add_to_proxy_file(self) -> None:
        #   Write out all successful connections to the file for storage.
        with open('proxies.txt', 'w+') as proxy_file:
            for address in self.connections:
                proxy_file.write(f'{address}\n')

    def read_from_proxy_file(self) -> None:
        #   Read all connections stored in the proxy file.
        #   Each gets added to self.connections so that the intrinsic properties of set() do not allow for duplicates.
        with open('proxies.txt', 'r+') as proxy_file:
            lines = proxy_file.readlines()
            for line in lines:
                self.connections.add(line.strip())

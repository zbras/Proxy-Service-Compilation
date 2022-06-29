from factory import ProxyService

class GeoNode(ProxyService):
    #   Subclass defining the GeoNode API service.
    def __init__(self):
        self.name = 'GEONODE'
        self.web_address = 'https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&google=true&protocols=https&anonymityLevel=elite&anonymityLevel=anonymous'
        self.resolve_type = 'data/json'
        super().__init__(self.web_address, self.resolve_type, self.name)

class PubProxy(ProxyService):
    #   Subclass defining the PubProxy API service.
    def __init__(self):
        self.name = 'PUBPROXY'
        self.web_address = 'http://pubproxy.com/api/proxy?https=true&level=elite&format=json&limit=5'
        self.resolve_type = 'data/json'
        super().__init__(self.web_address, self.resolve_type, self.name)

class ProxyScrape(ProxyService):
    #   Subclass defining the ProxyScrape API service.
    def __init__(self):
        self.name = 'PROXYSCRAPE'
        self.web_address = 'https://api.proxyscrape.com/v2?request=displayproxies&protocol=http&timeout=10000&country=us&ssl=yes&anonymity=elite'
        self.resolve_type = 'text'
        super().__init__(self.web_address, self.resolve_type, self.name)
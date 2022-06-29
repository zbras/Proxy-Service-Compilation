import requests as req

class Proxy():
    #   Class to check whether or not an IP and port address combination can be utilized as a proxy service.
    #   Attributes must be in the format 'x.x.x.x' for 'addr' and 'x' for 'port'.
    #   Call the check_service object method to return True (if the connection was successful) or False (if the connection was unsuccessful).

    def __init__(self, addr: str, port: str):
        #   Initializer function
        self.addr = addr
        self.port = port

    def check_service(self) -> bool:
        #   Returns True if the connection was successful, else will return False.
        try:
            req.get(
                'https://httpbin.org/ip',
                proxies = {
                    'http': f'{self.addr}:{self.port}',
                    'https': f'{self.addr}:{self.port}'
                },
                timeout = 3
            )

            return True

        except Exception as e:
            return False
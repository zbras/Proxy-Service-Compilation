
import os, sys

sys.path.insert(0, './modules')

from time import sleep
from services import *

def main():

    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        prox = PubProxy()
        prox = GeoNode()
        prox = ProxyScrape()
        sleep(60)

if __name__ == '__main__':

    main()

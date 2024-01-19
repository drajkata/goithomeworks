# Istnieje inny sposób na wykonanie kodu w osobnym wątku. Kod, który zostanie wykonany, musi zatem być funktorem (funkcją lub klasą, która posiada metodę __call__). Następnie obiekt może zostać przekazany jako argument nazwany target do Thread

from threading import Thread
from time import sleep
import logging

class UsefulClass():
    def __init__(self, second_num):
        self.delay = second_num

    def __call__(self):
        sleep(self.delay)
        logging.debug('Wake up!')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    t2 = UsefulClass(2)
    thread = Thread(target=t2)
    thread.start()
    print('Some stuff')

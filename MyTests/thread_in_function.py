# W procesie tworzenia instancji klasy Thread możemy przekazać argument do funkcji target i przekazać jej argumenty

from threading import Thread
from time import sleep
import logging

def example_work(delay):
    sleep(delay)
    logging.debug('Wake up!')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    for i in range(5):
        thread = Thread(target=example_work, args=(i,))
        thread.start()

# Argumenty przekazywane do funkcji są przekazywane jako krotka args w Thread. Nazwane argumenty funkcji mogą być również przekazywane jako słownik kwargs w Thread.

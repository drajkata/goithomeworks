import time
from multiprocessing import Process

def factorize(numbers):
    result = []
    for number in numbers:
        factorized_numbers = []
        for i in range(1, number + 1):
            if number % i == 0:
                factorized_numbers.append(i)
        result.append(factorized_numbers)
    return result

processes = []

for _ in range(4):
    processes.append(Process(target=factorize, args=([12, 18, 24])))

start = time.time()

for t in processes:
    t.start()

for t in processes:
    t.join()

stop = time.time()
print("Exec time for processes:", stop - start, "[s]")
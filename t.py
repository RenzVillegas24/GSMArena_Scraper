import time
import random

phone_sum = 60
total_time = 0

for j in range(phone_sum):
    start = time.time()
    time.sleep(random.randint(1000, 5000)/1000)
    end = time.time()

    total_time += end - start
    avg_time_per_iteration = total_time / (j + 1)
    remaining_iterations = phone_sum - (j + 1)
    remaining_time = avg_time_per_iteration * remaining_iterations
    
    eta = time.time() + remaining_time
    
    print(f"ETA: {time.strftime('%H:%M:%S', time.localtime(eta))}, Remaining Time: {time.strftime('%H:%M:%S', time.gmtime(remaining_time))}")

from enum import Enum
import datetime
import time
import random
#test tuples
# var_tuple = (1, "hi", "npi")
# print(var_tuple[2])

# var_list = list()
# print(len(var_list))

# for i in range(3):
#     print(i)
    
class Shake(Enum):
    YOLOv4Tiny = 7
    CHOCOLATE = 4
    COOKIES = 9
    MINT = 3

print(Shake(7) is Shake.YOLOv4Tiny)

test = {
    "name": "test" 
}

print(test["name"])

today = datetime.datetime.now()
hour = datetime.timedelta(minutes=1)
later = today + hour

time_now = time.time()
print(today)
print(later)
print(today>later)
print(time_now)

import multiprocessing 
 
print(multiprocessing.cpu_count())

random_number = random.randint(1, 10)
print(random_number)

elements = ["a", "b", "c"]
for i in range(len(elements)):
    print(i)
from enum import Enum
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
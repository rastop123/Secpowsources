#import math
from transformer import *

dict_value = {}
dict_value['U_c'] = input("Введите Uc:")
dict_value['schema'] = input("Введите schema:")
dict_value['U_21'] = input("Введите U_21:")
dict_value['U_31'] = input("Введите U_31:")
dict_value['U_22'] = input("Введите U_22:")
dict_value['I_21'] = input("Введите I_21")
dict_value['I_31'] = input("Введите I_31:")
dict_value['I_22'] = input("Введите I_22:")
dict_value['typesize'] = input("Введите typesize:")
dict_value['steelgrade'] = input("Введите steelgrade:")
t = Transformer(**dict_value)
result = t.calculate_all_value()
print(result)

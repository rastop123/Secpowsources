#import math
from transformer import *
from rectifier import *

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
for k in result.items():
    line = str(k[0]) + ' ' + str(k[1]) + "\n"
    file = open('/home/rastop/pyproject/replacer/value.txt', 'a')
    file.write(line)
    file.close()

rect_inp = {}
rect_inp['r_tr'] = input('Введите Rtr')
rect_inp['u_0'] = input('Введите U_O')
rect_inp['i_0'] = input('Введите I_O')
rect_inp['B_m'] = input('Введите B_m')
re = Rectifier(**rect_inp)
re_d = re.get_result_value()

for k in re_d.items():
    line = str(k[0]) + ' ' + str(k[1]) + "\n"
    file = open('/home/rastop/pyproject/replacer/value.txt', 'a')
    file.write(line)
    file.close()

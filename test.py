'''from rectifier import *


d = {'r_tr' : 1.2, 'u_0' : 5, 'i_0' : 3, 'B_m' : 1.3}
rect = Rectifier(**d)
rect.get_VD_params()
rect.get_r()
rect.get_parrams() '''


def module_n(x):
    if x >= 0:
        return x
    else:
        return -1 * x

def correct_fi(x):
    for i in range(1, 11):
        k = x - 15 * i
        if k <= 0:
            t = module_n(k)
            if t < 7.5:
                res = 15 * i
                return res
            else:
                res = 15 * i - 15
                return res

a = float(input())
print(correct_fi(a))
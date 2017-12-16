import math
import json

class Rectifier:

    m = 2
    f_c = 50
    K_l = 0.005
    s = 1 # Спросить у преподователя
    p = 2
    K_p1 = 0.05

    def __init__(self, **kwargs):
        self.r_tr = float(kwargs["r_tr"])
        self.U_0 = float(kwargs["u_0"])
        self.I_0 = float(kwargs["i_0"])
        self.B_m = float(kwargs["B_m"])

    def get_VD_params(self):
        self.u_VDobrm = float(input('Uобрм по приложению 3:'))
        self.u_VDpr = float(input('Upr по приложению 3:'))
        #self.i_VDprsr = float(input('Iпрср по приложению 3:'))
        self.i_VDprm = float(input('Iпрм по приложению 3:'))
        self.nameVD = input('Название Диода:')

    def get_r(self):
        self.r_pr = self.u_VDpr / self.i_VDprm
        self.r = self.r_tr + self.r_pr * 2

    def get_parrams(self):
        usqr = (self.U_0 * self.I_0) / (self.s * self.f_c * self.B_m)
        self.A = (math.pi * self.I_0 * self.r) / (self.U_0 * self.m)
        self.L_s = (self.K_l * self.s * self.U_0 * (usqr) ** (1 / 4)) / (((self.p - 1) ** 2) * self.I_0 * self.f_c * self.B_m)
        self.fi = math.atan((2 * math.pi * self.f_c * self.L_s) / self.r)
        self.fi = self.correct_fi(self.fi)
        self.B = self.get_value_json('B', self.A, self.fi)
        self.D = self.get_value_json('D', self.A, self.fi)
        self.F = self.get_value_json('F', self.A, self.fi)
        print('А равно:', self.A, 'Фи равно:', self.fi)
        self.H_02 = float(input('Введите H02:'))

    def get_value_rect(self):
        self.U_2 = self.B * self.U_0
        self.U_obrm = 1.5 * self.U_0
        self.I_prsr = 0.5 * self.I_0
        self.I_prm = 3.5 * self.I_0
        self.I_prVD = self.D * self.I_0
        self.I_2 = (self.D * self.I_0) / 1.42
        self.I1w1_I0w2 = self.D / 1.42
        self.S_tr = 1.5 * self.I_0 * self.U_0
        self.f_p1 = 2 * self.f_c
        self.S_2 = (self.B * self.D * self.I_0 * self.U_0) / 1.42
        self.S_1 = (self.B * self.D * self.I_0 * self.U_0) / 1.42
        self.C_1 = (100 * self.H_02) / (self.r * self.f_c * self.K_p1)
        print('Емкость расчетная равна:', self.C_1)
        self.C_1t = float(input('Введите емкость по приложению 4:'))

    def get_result_value(self):
        self.get_VD_params()
        self.get_r()
        self.get_parrams()
        self.get_value_rect()
        d = {}
        d['u_VDobrm'] = self.u_VDobrm
        d['u_VDpr'] = self.u_VDpr
        d['i_VDprm'] = self.i_VDprm
        d['nameVD'] = self.nameVD
        d['r_pr'] = self.r_pr
        d['r'] = self.r
        d['A'] = self.A
        d['B'] = self.B
        d['D'] = self.D
        d['F'] = self.F
        d['fi'] = self.fi
        d['L_s'] = self.L_s
        d['H_02'] = self.H_02
        d['U_2'] = self.U_2
        d['U_obrm'] = self.U_obrm
        d['I_prsr'] = self.I_prsr
        d['I_prm'] = self.I_prm
        d['I_prVD'] = self.I_prVD
        d['I_2'] = self.I_2
        d['I1w1_I0w2'] = self.I1w1_I0w2
        d['S_tr'] = self.S_tr
        d['f_p1'] = self.f_p1
        d['S_2'] = self.S_2
        d['S_1'] = self.S_1
        d['C_1'] = self.C_1
        d['C_1t'] = self.C_1t
        return d

    def get_value_json(self, n, a, f):
        file = open('graphs.json', 'r')
        value = json.loads(file.read())
        f = str(f)
        val = value[n][f]
        l = len(val)
        for i in range(0, l):
            if a > val[i][0]:
                if a <= val[i + 1][0]:
                    final_value = val[i][1] + ((a - val[i][0]) / (val[i + 1][0] - val[i][0])) * (
                    val[i + 1][1] - val[i][1])
                    return final_value
        else:
            return val[l - 1][1]

    def correct_fi(self, x):
        for i in range(1, 11):
            k = x - 15 * i
            if k <= 0:
                t = self.module_n(k)
                if t < 7.5:
                    res = 15 * i
                    return res
                else:
                    res = 15 * i -15
                    return res

    def module_n(self, x):
        if x >= 0:
            return x
        else:
            return -1 * x
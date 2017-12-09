import math

class stabilizer:

    u_kevt2min = 2
    u_rzash = 0.6
    kp1 = None # у преподавателя узнать
    r_0 = 2.5
    fc = 50

    def __init__(self, **kwargs):
        self.u_in = float(kwargs['u_in'])
        self.a_max = float(kwargs['a_max'])
        self.a_min = float(kwargs['a_min'])
        self.u_out = float(kwargs['u_out'])
        self.i_nmax = float(kwargs['i_nmax'])
        self.i_nmin = float(kwargs['i_nmin'])
        self.kc_mu = float(kwargs['kc_mu'])
        self.u_outm = float(kwargs['u_outm'])

    def calculate_value(self):
        self.u_inmina = self.u_in * (1 - self.a_min)
        self.u_inm1 = self.u_in * self.kp1
        self.u_in1 = self.r_0 * self.i_nmax
        self.u_inismin = self.u_inmina - self.u_kevt2min - self.u_inm1 - self.u_rzash - self.u_in1
        self.u_inmaxa = self.u_in * (1 - self.a_max)
        self.u_inmaxi = self.u_inmaxa + self.u_inm1 + self.r_0 * (self.i_nmax - self.i_nmin)
        self.i_kvt2max = self.i_nmax
        self.u_kevt2max = self.u_inmaxi - self.u_outm - self.diff_u_ismin # спросить у преподователя и уточнить по поводу U вых
        self.p_vt2max = self.u_kevt2max * self.i_kvt2max
        self.u_vd1min = self.diff_u_cmmin + self.u_r3 +self.u_bevt1vt2 #Опять ничего не известно)
        self.i_bevt1vt2max = self.i_nmax / self.b_vt1vt2 #Еще кое что узнать
        self.r1 = (self.u_inmina - self.u_inm1 - self.u_out) / (self.i_vd1min + self.i_bevt1vt2max) #тоже узнать
        self.p_r1 = (self.u_inmaxi - self.u_vd1 - self.u_out) * (self.i_vd1min + self.i_bevt1vt2max)
        self.i_vd1max = (self.u_inmax - self.u_out - self.u_vd1) / self.r1
        self.p_vd1max = self.u_vd1 * self.i_vd1max
        self.r4r5 = self.u_outis / self.i_r4r5
        self.r4 = self.u_outis / self.i_r4r5
        self.r5 = self.r4
        self.p_r4 = (self.i_r4r5 ** 2) * self.r4
        self.r3 = self.u_bevt1vt2 / self.i_nmax
        self.p_r3 = self.u_bevt1vt2 * self.i_nmax
        self.c = 1 / (0.1 * self.r5 * 2 * math.pi * self.fc)
        print('Емкость расчетная равна:', self.c)
        self.ct = float(input('Введите емкость по приложению 4:'))

    def get_user_vt2_params(self):
        pass

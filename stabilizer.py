import math

class stabilizer:

    u_kevt2min = 2
    u_rzash = 0.6
    kp1 = None # у преподавателя узнать
    r_0 = 2.5

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
        self.u_kevt2max = self.u_inmaxi - self.u_outmin - self.diff_u_ismin # спросить у преподователя
        self.p_vt2max = self.u_kevt2max * self.i_kvt2max

    def get_user_vt2_params(self):
        pass

    def

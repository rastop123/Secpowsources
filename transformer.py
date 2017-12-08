import math

class Transformer:

    H_from_B_m = ((1.5, 80), (1.6, 150), (1.7, 250), (2, 600))
    P_yd_from_B_m = ((1, 1), (1.2, 1.3), (1.4, 2), (1.7, 3))
    j_from_P2 = ((0, 1.4), (40, 2.5), (60, 2.6), (150, 2.3), (400, 2), (2000, 2))
    k0_from_P2_100 = ((0, 0.2), (20, 0.26), (60, 0.31), (100, 0.33), (140, 0.345), (180, 0.35), (2000, 0.36))
    k0_from_P2_300 = ((0, 0.18), (20, 0.225), (60, 0.275), (100, 0.3), (140, 0.3), (180, 0.305), (2000, 0.31))
    B_m_from_P2 = ((0, 1.5), (40, 1.5), (60, 1.6), (2000, 1.7))
    U_diff_from_P2 = ((25, 0.12), (50, 0.11), (100, 0.09), (150, 0.072), (200, 0.06), (250, 0.055), (300, 0.05), (2000, 0.042))
    k_c = float('0.93')

    def __init__(self, **kwargs):
        self.U_c = float(kwargs["U_c"])
        self.schema = kwargs["schema"]
        self.U_21 = float(kwargs["U_21"])
        self.U_31 = float(kwargs["U_31"])
        self.U_22 = float(kwargs["U_22"])
        self.I_21 = float(kwargs["I_21"])
        self.I_22 = float(kwargs["I_22"])
        self.I_31 = float(kwargs["I_31"])
        self.typesize = kwargs["typesize"]
        self.steelgrade = kwargs["steelgrade"]
        self.w_21 = 0
        self.w_22 = 0
        self.w_31 = 0
        self.w_32 = 0
        self.q_21 = 0
        self.q_22 = 0
        self.q_31 = 0
        self.q_32 = 0
        self.d_21 = 0
        self.d_22 = 0
        self.d_31 = 0
        self.d_32 = 0
        self.d_21_i = 0
        self.d_22_i = 0
        self.d_31_i = 0
        self.d_32_i = 0
        self.g_21 = 0
        self.g_22 = 0
        self.g_31 = 0
        self.g_32 = 0
        self.s_21 = 0
        self.s_22 = 0
        self.s_31 = 0
        self.s_32 = 0
        self.j_21 = 0
        self.j_22 = 0
        self.j_31 = 0
        self.j_32 = 0
        self.ky_21 = 0
        self.ky_22 = 0
        self.ky_31 = 0
        self.ky_32 = 0
        self.w_sl_21 = 0
        self.w_sl_22 = 0
        self.w_sl_31 = 0
        self.w_sl_32 = 0
        self.n_sl_21 = 0
        self.n_sl_22 = 0
        self.n_sl_31 = 0
        self.n_sl_32 = 0
        self.sigma_21 = 0
        self.sigma_22 = 0
        self.sigma_31 = 0
        self.sigma_32 = 0
        self.r_sr_21 = 0
        self.r_sr_22 = 0
        self.r_sr_31 = 0
        self.r_sr_32 = 0
        self.l_sr_21 = 0
        self.l_sr_22 = 0
        self.l_sr_31 = 0
        self.l_sr_32 = 0
        self.r_om_21 = 0
        self.r_om_22 = 0
        self.r_om_31 = 0
        self.r_om_32 = 0





    def overpower(self):
        if self.schema in ("а", "б"):
            self.sec_power = (self.U_21 * self.I_21) + 2 * (self.U_31 * self.I_31 + self.U_31 * self.I_31)
        elif self.schema == "в":
            self.sec_power = 2 * (self.U_21 * self.I_21 + self.U_22 * self.I_22)

    def effic(self):
        self.kpd = math.tanh(1.14 + 0.024 * self.sec_power)

    def ratepower(self):
        self.temp_1 = math.sqrt(2) * (1 + self.kpd) * (self.U_21 * self.I_21)
        self.temp_2 = 2 * (1 + math.sqrt(2 * self.kpd)) * (self.U_31 * self.I_31 + self.U_31 * self.I_31)
        self.temp_3 = 2 * (1 + math.sqrt(2 * self.kpd)) * (self.U_21 * self.I_21 + self.U_22 * self.I_22)
        if self.schema == "б":
            self.rp = ((1 + self.kpd) / (2 * self.kpd)) * self.sec_power
        elif self.schema == "а":
            self.rp = (math.sqrt(2) / (4 * self.kpd)) * (self.temp_1 + self.temp_2)
        elif self.schema == "в":
            self.rp = (math.sqrt(2) / (4 * self.kpd)) * self.temp_3

        del self.temp_1
        del self.temp_2
        del self.temp_3

# Функции для получения B_m j k_c k_o P_yd G_c U_diff --- k_c = 0.93

    def get_j(self):
        self.j = self.get_value_of_graph(self.sec_power, *self.j_from_P2) # Уточнить по поводу мощности

    def get_k0(self):
        if self.U_c <= 300:
            if self.U_c <= 100:
                self.k_o = self.get_value_of_graph(self.sec_power, *self.k0_from_P2_100)
            else:
                self.k_o = self.get_value_of_graph(self.sec_power, *self.k0_from_P2_300)

    def get_B_m(self):
        self.B_m = self.get_value_of_graph(self.sec_power, *self.B_m_from_P2)

    def get_U_diff(self):
        self.U_diff = self.get_value_of_graph(self.sec_power, *self.U_diff_from_P2)

    def get_sc_so(self):
        self.sc_so = (50 * self.rp) / (50 * self.B_m * self.j * self.k_c * self.k_o * 1.1)

    def get_user_param(self):  # Получаем значения из таблицы
        self.S_c = float(input("Введите S_c: "))
        self.l_sr = float(input("Введите l_sr: "))
        self.V_c = float(input("Введите V_c: "))
        m = float(input("Введите G_c: "))
        self.G_c = m / 1000
        self.lw_sr = float(input("Введите lw_sr: "))
        self.h_table = float(input("Введите h_table: "))
        self.sigma_0 = float(input("Введите Сигму 0:"))
        self.a_table = float(input("ВВедите а:"))
        self.b_table = float(input("ВВедите b:"))

    def get_w_0(self):
        self.w_0 = 10000 / (4 * self.B_m * 50 * self.S_c * self.k_c * 1.1) # Уточнить по поводу k_o

    def get_w(self):
        self.w_11 = self.w_0 * self.U_c * (1 - 0.5 * self.U_diff)
        if self.schema == "а":
            self.w_21 = self.w_0 * self.U_21 * (1 - 0.5 * self.U_diff)
            self.w_31 = self.w_0 * self.U_31 * (1 - 0.5 * self.U_diff)
            self.w_32 = self.w_0 * self.U_31 * (1 - 0.5 * self.U_diff)
        elif self.schema == "б":
            self.w_21 = self.w_0 * self.U_21 * (1 - 0.5 * self.U_diff)
        elif self.schema == "в":
            self.w_21 = self.w_0 * self.U_21 * (1 - 0.5 * self.U_diff)
            self.w_22 = self.w_0 * self.U_22 * (1 - 0.5 * self.U_diff)

    def get_P_c(self):
        P_yd = self.get_value_of_graph(self.B_m, *self.P_yd_from_B_m)
        self.P_c = P_yd * self.G_c

    def get_I_xx(self):
        self.H_m = self.get_value_of_graph(self.B_m, *self.H_from_B_m)
        self.I_xxa = self.P_c / (self.U_c * (1 - 0.5 * self.U_diff))
        self.I_xxr = (self.H_m * self.l_sr * 0.01) / self.w_11 + (0.8 * self.B_m * 2 * 0.002 * 10000) / (math.sqrt(2) * self.w_11)
        self.I_xx = math.sqrt(self.I_xxa ** 2 + self.I_xxr ** 2)

    def get_I_11(self):
        if self.schema == "а":
            var1 = self.calc_1(self.I_31, self.w_31, self.w_11)
            var2 = self.calc_1(self.I_21, self.w_21, self.w_11)
            self.I_11 = math.sqrt(4 * var1 + var2 + self.I_xx ** 2)
        elif self.schema == "б":
            var2 = self.calc_1(self.I_21, self.w_21, self.w_11)
            self.I_11 = math.sqrt(var2 + self.I_xx ** 2)
        elif self.schema == "в":
            var1 = self.calc_1(self.I_21, self.w_21, self.w_11)
            self.I_11 = math.sqrt(4 * var1 + self.I_xx ** 2)

    def get_q(self):
        self.q_11 = self.I_11 / self.j
        if self.schema == "а":
            self.q_21 = self.I_21 / self.j
            self.q_31 = self.I_31 / self.j
            self.q_32 = self.I_31 / self.j
        elif self.schema == "б":
            self.q_21 = self.I_21 / self.j
        elif self.schema == "в":
            self.q_21 = self.I_21 / self.j
            self.q_22 = self.I_22 / self.j

    def get_wire_param(self):
        print("Площадь равна", self.q_11)
        self.d_11 = float(input("Введите Значение d с изоляцией "))
        self.d_11_i = float(input("Введите Значение d без изоляции "))
        self.g_11 = float(input("Введите Значение m Одного метра "))
        if self.schema == "а":
            print("площадь равна", self.q_21)
            self.d_21 = float(input("Введите Значение d с изоляцией "))
            self.d_21_i = float(input("Введите Значение d без изоляции "))
            self.g_21 = float(input("Введите Значение m Одного метра "))
            print("площадь равна", self.q_31)
            self.d_31 = float(input("Введите Значение d с изоляцией "))
            self.d_31_i = float(input("Введите Значение d без изоляции "))
            self.g_31 = float(input("Введите Значение m Одного метра "))
            self.d_32 = self.d_31
            self.d_32_i = self.d_31_i
            self.g_32 = self.g_31
        elif self.schema == "б":
            print("площадь равна", self.q_21)
            self.d_21 = float(input("Введите Значение d с изоляцией "))
            self.d_21_i = float(input("Введите Значение d без изоляции "))
            self.g_21 = float(input("Введите Значение m Одного метра "))
        elif self.schema == "в":
            print("площадь равна", self.q_21)
            self.d_21 = float(input("Введите Значение d с изоляцией "))
            self.d_21_i = float(input("Введите Значение d без изоляции "))
            self.g_21 = float(input("Введите Значение m Одного метра "))
            self.d_22 = self.d_21
            self.d_22_i = self.d_21_i
            self.g_22 = self.g_21

    def get_area(self):
        self.s_11 = ((self.d_11 ** 2) * math.pi) / 4
        if self.schema == "а":
            self.s_21 = ((self.d_21 ** 2) * math.pi) / 4
            self.s_31 = ((self.d_31 ** 2) * math.pi) / 4
            self.s_32 = ((self.d_32 ** 2) * math.pi) / 4
        elif self.schema == "б":
            self.s_21 = ((self.d_21 ** 2) * math.pi) / 4
        elif self.schema == "в":
            self.s_21 = ((self.d_21 ** 2) * math.pi) / 4
            self.s_22 = ((self.d_22 ** 2) * math.pi) / 4

    def j_real(self):
        self.j_11 = self.I_11 / self.s_11
        if self.schema == "а":
            self.j_21 = self.I_21 / self.s_21
            self.j_31 = self.I_31 / self.s_31
            self.j_32 = self.I_31 / self.s_32
        elif self.schema == "б":
            self.j_21 = self.I_21 / self.s_21
        elif self.schema == "в":
            self.j_21 = self.I_21 / self.s_21
            self.j_22 = self.I_22 / self.s_22



    def get_j_mean(self):
        if self.schema == "а":
            self.j_mean = self.calc_mean_value(self.j_11, self.j_21, self.j_31, self.j_32)
        elif self.schema == "б":
            self.j_mean = self.calc_mean_value(self.j_11, self.j_21)
        elif self.schema == "в":
            self.j_mean = self.calc_mean_value(self.j_11, self.j_21, self.j_22)

    def get_hob_11(self):
        self.hob_11 = self.h_table - 5.5

    def get_ky(self):
        k = []
        d_all = (self.d_11_i, self.d_21_i, self.d_22_i, self.d_31_i, self.d_32_i)
        for i in range(0, 5):
            if d_all[i] == 0:
                k.append(0)
            elif d_all[i] <= 0.2:
                k.append(0.9)
            elif d_all[i] <= 0.5:
                k.append(0.93)
            elif d_all[i] <= 0.8:
                k.append(0.95)
            elif d_all[i] < 1:
                k.append(0.9)
            elif d_all[i] >= 1:
                k.append(0.85)
        self.ky_11 = k[0]
        self.ky_21 = k[1]
        self.ky_22 = k[2]
        self.ky_31 = k[3]
        self.ky_32 = k[4]

    def get_w_sl(self):
        self.w_sl_1 = (self.hob_11 * self.ky_11) / self.d_11_i
        if self.schema == "а":
            self.w_sl_21 = (self.hob_11 * self.ky_21) / self.d_21_i
            self.w_sl_31 = (self.hob_11 * self.ky_31) / self.d_31_i
            self.w_sl_32 = (self.hob_11 * self.ky_32) / self.d_32_i
        elif self.schema == "б":
            self.w_sl_21 = (self.hob_11 * self.ky_21) / self.d_21_i
        elif self.schema == "в":
            self.w_sl_21 = (self.hob_11 * self.ky_21) / self.d_21_i
            self.w_sl_22 = (self.hob_11 * self.ky_22) / self.d_22_i

    def get_m_kf(self):
        if self.typesize == "ШЛ":
            self.m_kf = 1
        elif self.typesize == "ПЛ":
            self.m_kf = 2

    def get_n_sl(self):
        self.n_sl_11 = (1 / self.m_kf) * (self.w_11 / self.w_sl_1)
        if self.schema == "а":
            self.n_sl_21 = (1 / self.m_kf) * (self.w_21 / self.w_sl_21)
            self.n_sl_31 = (1 / self.m_kf) * (self.w_31 / self.w_sl_31)
            self.n_sl_32 = (1 / self.m_kf) * (self.w_32 / self.w_sl_32)
        elif self.schema == "б":
            self.n_sl_21 = (1 / self.m_kf) * (self.w_21 / self.w_sl_21)
        elif self.schema == "в":
            self.n_sl_21 = (1 / self.m_kf) * (self.w_21 / self.w_sl_21)
            self.n_sl_22 = (1 / self.m_kf) * (self.w_22 / self.w_sl_22)

    def get_sigma(self):
        self.sigma_1 = 1.2 * self.n_sl_11 * self.d_11
        self.sigma_21 = 1.2 * self.n_sl_21 * self.d_21
        self.sigma_22 = 1.2 * self.n_sl_22 * self.d_22
        self.sigma_31 = 1.2 * self.n_sl_31 * self.d_31
        self.sigma_32 = 1.2 * self.n_sl_32 * self.d_32
        if self.schema == "а":
            self.sigma_p = self.sigma_1 + self.sigma_21 + self.sigma_31 + self.sigma_32 + 2 * self.sigma_0
        elif self.schema == "б":
            self.sigma_p = self.sigma_1 + self.sigma_21 + 2 * self.sigma_0
        elif self.schema == "в":
            self.sigma_p = self.sigma_1 + self.sigma_21 + self.sigma_22 + 2 * self.sigma_0

    def get_r_sr(self):
        self.r_sr_1 = 2.75 + self.sigma_1 / 2
        if self.schema == "а":
            self.r_sr_21 = 2.75 + self.sigma_0 + self.sigma_1 + self.sigma_21 + self.sigma_31 + self.sigma_32 - self.sigma_21 / 2
            self.r_sr_31 = 2.75 + 2 * self.sigma_0 + self.sigma_1 + self.sigma_21 + self.sigma_31 + self.sigma_32 - self.sigma_31 / 2
            self.r_sr_32 = 2.75 + 2 * self.sigma_0 + self.sigma_1 + self.sigma_21 + self.sigma_31 + self.sigma_32 - self.sigma_32 / 2
        elif self.schema == "б":
            self.r_sr_21 = 2.75 + self.sigma_0 + self.sigma_1 + self.sigma_21 - self.sigma_21 / 2
        elif self.schema == "в":
            self.r_sr_21 = 2.75 + self.sigma_0 + self.sigma_1 + self.sigma_21 + self.sigma_22 - self.sigma_21 / 2
            self.r_sr_22 = 2.75 + self.sigma_0 + self.sigma_1 + self.sigma_21 + self.sigma_22 - self.sigma_22 / 2

    def get_l_sr(self):
        self.l_sr_1 = (2 * (self.a_table + self.b_table + math.pi * self.r_sr_1)) / 1000
        if self.schema == "а":
            self.l_sr_21 = (2 * (self.a_table + self.b_table + math.pi * self.r_sr_21)) / 1000
            self.l_sr_31 = (2 * (self.a_table + self.b_table + math.pi * self.r_sr_31)) / 1000
            self.l_sr_32 = (2 * (self.a_table + self.b_table + math.pi * self.r_sr_32)) / 1000
        elif self.schema == "б":
            self.l_sr_21 = (2 * (self.a_table + self.b_table + math.pi * self.r_sr_21)) / 1000
        elif self.schema == "в":
            self.l_sr_21 = (2 * (self.a_table + self.b_table + math.pi * self.r_sr_21)) / 1000
            self.l_sr_22 = (2 * (self.a_table + self.b_table + math.pi * self.r_sr_22)) / 1000

    def get_r_om(self):
        self.r_om_1 = (self.l_sr_1 * self.w_11 * 1.28) / (57 * self.q_11)
        if self.schema == "а":
            self.r_om_21 = (self.l_sr_21 * self.w_21 * 1.28) / (57 * self.q_21)
            self.r_om_31 = (self.l_sr_31 * self.w_31 * 1.28) / (57 * self.q_31)
            self.r_om_32 = (self.l_sr_32 * self.w_32 * 1.28) / (57 * self.q_32)
        elif self.schema == "б":
            self.r_om_21 = (self.l_sr_21 * self.w_21 * 1.28) / (57 * self.q_21)
        elif self.schema == "в":
            self.r_om_21 = (self.l_sr_21 * self.w_21 * 1.28) / (57 * self.q_21)
            self.r_om_22 = (self.l_sr_22 * self.w_22 * 1.28) / (57 * self.q_22)

    def get_loss_copper(self):
        self.p_loss_1 = (self.I_11 ** 2) * self.r_om_1
        self.p_loss_21 = (self.I_21 ** 2) * self.r_om_21
        self.p_loss_22 = (self.I_22 ** 2) * self.r_om_22
        self.p_loss_31 = (self.I_31 ** 2) * self.r_om_31
        self.p_loss_32 = (self.I_31 ** 2) * self.r_om_32
        if self.schema == "а":
            self.p_loss = self.p_loss_1 + self.p_loss_21 + self.p_loss_31 + self.p_loss_32
        elif self.schema == "б":
            self.p_loss = self.p_loss_1 + self.p_loss_21
        elif self.schema == "в":
            self.p_loss = self.p_loss_1 + self.p_loss_21 + self.p_loss_22

    def get_real_kpd(self):
        self.real_kpd = self.sec_power / (self.p_loss + self.P_c + self.sec_power)

    def calc_1(self, x, y, z):
        res = ((x * y) / z ) ** 2
        return res

    def get_value_of_graph(self, x, *rv):
        x = float(x)
        l = len(rv)
        for i in range(0, l):
            if x >= rv[i][0]:
                if x <= rv[i + 1][0]:
                    final_value = rv[i][1] + ((x - rv[i][0]) / (rv[i + 1][0] - rv[i][0])) * (rv[i + 1][1] - rv[i][1])
                    return final_value
        else:
            pass

    def calc_mean_value(self, *args):
        l = len(args)
        u = 1
        for i in args:
            u = u * i
        else:
            pass
        res = u ** (1 / l)
        return  res

    def calculate_all_value(self):
        self.overpower()
        self.effic()
        self.ratepower()
        self.get_j()
        self.get_k0()
        self.get_B_m()
        self.get_U_diff()
        self.get_sc_so()
        print(self.sc_so)
        self.get_user_param()
        self.get_w_0()
        self.get_w()
        self.get_P_c()
        self.get_I_xx()
        self.get_I_11()
        self.get_q()
        self.get_wire_param()
        self.get_area()
        self.j_real()
        self.get_j_mean()
        self.get_hob_11()
        self.get_ky()
        self.get_w_sl()
        self.get_m_kf()
        self.get_n_sl()
        self.get_sigma()
        self.get_r_sr()
        self.get_l_sr()
        self.get_r_om()
        self.get_loss_copper()
        self.get_real_kpd()
        d = {}
        d['P2'] = round(self.sec_power, 2)
        d['kpd'] = round(self.kpd, 2)
        d['Pras'] = round(self.rp, 2)
        d['j'] = round(self.j, 2)
        d['B_m'] = round(self.B_m, 2)
        d['U_diff'] = round(self.U_diff, 2)
        d['sc_so'] = round(self.sc_so, 2)
        d['w_0'] = round(self.w_0, 2)
        d['w_21'] = round(self.w_21, 2)
        d['w_22'] = round(self.w_22, 2)
        d['w_31'] = round(self.w_31, 2)
        d['w_32'] = round(self.w_32, 2)
        d['w_11'] = round(self.w_11, 2)
        d['P_c'] = round(self.P_c, 2)
        d['H_m'] = round(self.H_m, 2)
        d['I_xxr'] = round(self.I_xxr, 2)
        d['I_xxa'] = round(self.I_xxa, 2)
        d['I_xx'] = round(self.I_xx, 2)
        d['I_11'] = round(self.I_11, 2)
        d['q_11'] = round(self.q_11, 2)
        d['q_21'] = round(self.q_21, 2)
        d['q_22'] = round(self.q_22, 2)
        d['q_31'] = round(self.q_31, 2)
        d['q_32'] = round(self.q_32, 2)
        d['s_11'] = round(self.s_11, 2)
        d['s_21'] = round(self.s_21, 2)
        d['s_22'] = round(self.s_22, 2)
        d['s_31'] = round(self.s_31, 2)
        d['s_32'] = round(self.s_32, 2)
        d['j_11'] = round(self.j_11, 2)
        d['j_21'] = round(self.j_21, 2)
        d['j_22'] = round(self.j_22, 2)
        d['j_31'] = round(self.j_31, 2)
        d['j_32'] = round(self.j_32, 2)
        d['j_sr'] = round(self.j_mean, 2)
        d['hob_11'] = round(self.hob_11, 2)
        d['ky_11'] = round(self.ky_11, 2)
        d['ky_21'] = round(self.ky_21, 2)
        d['ky_22'] = round(self.ky_22, 2)
        d['ky_31'] = round(self.ky_31, 2)
        d['ky_32'] = round(self.ky_32, 2)
        d['w_sl_1'] = round(self.w_sl_1, 2)
        d['w_sl_21'] = round(self.w_sl_21, 2)
        d['w_sl_22'] = round(self.w_sl_22, 2)
        d['w_sl_31'] = round(self.w_sl_31, 2)
        d['w_sl_32'] = round(self.w_sl_32, 2)
        d['m_kf'] = round(self.m_kf, 2)
        d['n_sl_11'] = round(self.n_sl_11, 2)
        d['n_sl_21'] = round(self.n_sl_21, 2)
        d['n_sl_22'] = round(self.n_sl_22, 2)
        d['n_sl_31'] = round(self.n_sl_31, 2)
        d['n_sl_32'] = round(self.n_sl_32, 2)
        d['sigma_1'] = round(self.sigma_1, 2)
        d['sigma_21'] = round(self.sigma_21, 2)
        d['sigma_22'] = round(self.sigma_22, 2)
        d['sigma_31'] = round(self.sigma_31, 2)
        d['sigma_32'] = round(self.sigma_32, 2)
        d['sigma_p'] = round(self.sigma_p, 2)
        d['r_sr_1'] = round(self.r_sr_1, 2)
        d['r_sr_21'] = round(self.r_sr_21, 2)
        d['r_sr_22'] = round(self.r_sr_22, 2)
        d['r_sr_31'] = round(self.r_sr_31, 2)
        d['r_sr_32'] = round(self.r_sr_32, 2)
        d['l_sr_1'] = round(self.l_sr_1, 2)
        d['l_sr_21'] = round(self.l_sr_21, 2)
        d['l_sr_22'] = round(self.l_sr_22, 2)
        d['l_sr_31'] = round(self.l_sr_31, 2)
        d['l_sr_32'] = round(self.l_sr_32, 2)
        d['r_om_1'] = round(self.r_om_1, 2)
        d['r_om_21'] = round(self.r_om_21, 2)
        d['r_om_22'] = round(self.r_om_22, 2)
        d['r_om_31'] = round(self.r_om_31, 2)
        d['r_om_32'] = round(self.r_om_32, 2)
        d['p_loss_1'] = round(self.p_loss_1, 2)
        d['p_loss_21'] = round(self.p_loss_21, 2)
        d['p_loss_22'] = round(self.p_loss_22, 2)
        d['p_loss_31'] = round(self.p_loss_31, 2)
        d['p_loss_32'] = round(self.p_loss_32, 2)
        d['p_loss'] = round(self.p_loss, 2)
        d['real_kpd'] = round(self.real_kpd, 2)
        return d
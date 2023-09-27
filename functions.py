from statistics import mean, variance
from math import exp, sqrt, floor
from numpy import linspace
from scipy.interpolate import griddata


def interpolate(time, V_component, num_pontos, method_in):
    interp_time = linspace(min(time), max(time), num_pontos)
    interp_values = griddata(time, V_component, interp_time, method=method_in, fill_value=0)
    return interp_time, interp_values


def advance_samples(time, V_source, V_component, V_in):
    flag = False
    
    for value in V_source:
        if value < 0: value = 0

    if V_source[0] < 0.5*V_in:
        for key, value in enumerate(V_source):
            if value > 0.5*V_in:
                advance_until = (key-1)
                break

    if V_source[0] > 0.5*V_in:
        for key, value in enumerate(V_source):
            if value < 0.5*V_in:
                flag = True
            if (value > 0.5*V_in) and flag:
                advance_until = (key-1)
                break

    return time[advance_until:], V_source[advance_until:], V_component[advance_until:]


def check_type_component(V_in, V_component):
    media = mean(V_component)
    negative = False

    for value in V_component:
        if value < 0:
            negative = True
            break

    if negative and ((media > -0.1*V_in) and (media < 0.1*V_in)):
        return "inductor"
    elif media > (1/3*V_in):
        return "capacitor"
    else:
        return None


def check_half_period(time, V_source, V_in):
    start_time = time[0]
    previous_value = V_source[0]

    for key, value in enumerate(V_source[1:]):
        
        if (value<=0.01*V_in) and (previous_value>=0.99*V_in):
            return (time[key] - start_time)

        previous_value = value

    return None
                

def check_amount_periods(time, half_period):
    amt_per = (max(time) - min(time))/(2*half_period)
    if amt_per <= 3.9:  return "fewPeriods"         #4 periods
    if amt_per >= 12.1: return "manyPeriods"        #12 periods
    return floor(amt_per)


def check_charge_component(component, V_in, V_component, time,  half_period, tau_threshroad=4):
    threshroad_cap = (1 - exp(-tau_threshroad))
    threshroad_ind = exp(-tau_threshroad)
    div_per_cap = 18
    div_per_ind = 18
    tau_time_cap = None
    tau_time_ind = None
    
    if component == "capacitor":

        #Verifica se o capacitor é muito grande (de acordo com a frequência)
        for key, value in enumerate(V_component):
            if value > threshroad_cap*V_in:
                break
            elif (key == len(V_component) - 1):
                return "largeCapacitor"

        #Verifica se o capacitor é extremamente pequeno (de acordo com a frequência)
        media = mean(V_component)
        dp = sqrt(variance(V_component))
        if((media>=0.495*V_in) and (media<=0.505*V_in)) and((dp>=0.495*V_in) and (dp<=0.505*V_in)):
            return "extremeSmallCapacitor"

        #Verifica se o capacitor é muito pequeno (de acordo com a frequência)
        for key, value in enumerate(V_component):
            if (value >= V_in*0.612) and (value <= V_in*0.652):
                if time[key] <= half_period/div_per_cap:
                    return "smallCapacitor"
                else:
                    tau_time_cap = time[key]
                    break
        
        return tau_time_cap

    if component == "indutor":

        print("Maximo: ", max(V_component))
        #Checa se o indutor é muito grande, checa a constante de tempo passada como parametro (de acordo com a frequência)
        for key, value in enumerate(V_component):
            if (abs(time[key] - half_period) <= half_period/20):
                if value > V_in*threshroad_ind:
                    return "largeInductor"
                else:
                    break
        
        #Lida com o caso de indutores extremamente pequenos (de acordo com a frequência)
        for key, value in enumerate(V_component):
            if value > 0.5*V_in:
                break
            elif (key == len(V_component) - 1):
                return "extremeSmallInductor"

        #Lida com o caso de indutores pequenos mas que se consegue ter algum nível de curva (de acordo com a frequência)
        for key, value in enumerate(V_component):
            if (value >= 0.348*V_in) and (value <= 0.388*V_in):
                if time[key] <= half_period/div_per_ind:
                    return "smallInductor"
                else:
                    tau_time_ind = time[key]
                    break

        return tau_time_ind
    
    return None


def get_value(component, tau_time, resistor):
    if component == "capacitor": return tau_time/resistor
    elif component == "indutor": return tau_time*resistor
    else: return None


def format_number(number):
    qtd_mlt = 0
    if number < 1:
        while (number<1):
            number *= 10
            qtd_mlt += 1
    else: return "outOfRange"

    qct, resto = divmod(qtd_mlt, 3)

    if (qct==0) or (qct==1 and resto==0):
        new_number = str(round(number*relatione(resto), 2)) + 'm'
    elif (qct==1) or (qct==2 and resto==0):
        new_number = str(round(number*relatione(resto), 2)) + 'µ'
    elif (qct==2) or (qct==3 and resto==0):
        new_number = str(round(number*relatione(resto), 2)) + 'n'
    elif (qct==3) or (qct==4 and resto==0):
        new_number = str(round(number*relatione(resto), 2)) + 'p'
    else:
        return "outOfRange"
    
    return new_number


def relatione(num):
    if num==2:
        return 10
    elif num==1:
        return 100
    elif num==0:
        return 1
    else:
        return None
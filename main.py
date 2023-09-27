from class_component import Capacitor_Indutor
import functions as func
import matplotlib.pyplot as plt

component = Capacitor_Indutor(origin="simulator", resistor=1000, V_in=5, tau=4)
pts_interp = 10000
type_intp_Vcomp = "linear"
type_intp_Vsrc = "linear"

while True:

    #Pause
    input("Tecle enter para iniciar/reiniciar.\n")

    #Chamar o método da aquisição de dados
    if component.origin == "simulator":
        component.simulator()
    elif component.origin == "oscilloscope":
        component.oscilloscope()
    else:
        print("Origem de captura não conhecida.")
        continue

    #Interpolação dos dados
    interp_time, interp_V_component = func.interpolate(component.time, component.V_component, pts_interp, type_intp_Vcomp)
    _,           interp_V_source    = func.interpolate(component.time, component.V_source, pts_interp, type_intp_Vsrc)

    #Forçar o avanço da primeira amostra para o começo de um período inteiro
    new_time, new_V_source, new_V_component = func.advance_samples(interp_time, interp_V_source, interp_V_component, component.V_in)

    #Descobrir o tipo de componente (capacitor ou indutor) e salvar
    type_component = func.check_type_component(component.V_in, new_V_component)
    if type_component != None:
        component.type = type_component 
    else:
        print("Componente não reconhecido.")
        continue

    #Calcular a metade de um período da onda quadrada de teste
    half_period = func.check_half_period(new_time, new_V_source, component.V_in)
    if half_period == None:
        print("Não se conseguiu calcular o meio período")
        continue
    print_half_period = func.format_number(half_period)
    if print_half_period == "outOfRange":
        print("Formatação do meio período fora do range (m, µ, n, p).")
        continue
    print("Meio periodo: ", print_half_period, end='s\n')

    #Calcular a quantidade de períodos totais
    qtd_periodos = func.check_amount_periods(new_time, half_period)
    if qtd_periodos == "fewPeriods":
        print("Poucos períodos, aumente a quantidade (4-12)!")
        continue
    elif qtd_periodos == "manyPeriods":
        print("Muitos períodos, diminua a quantidade (4-12)!")
        continue
    print("Qtd periodos: ", qtd_periodos)

    #Checar o tamanho dos componentes, pequeno ou grande, se for aceitável, retorna o tempo do primeiro tau.
    checar_componente = func.check_charge_component(component.type, component.V_in, new_V_component, new_time, half_period, component.tau)
    if checar_componente == "largeCapacitor":
        print("Capacitor grande, diminua a frequência!")
        continue
    elif checar_componente == "smallCapacitor":
        print("Capacitor pequeno, aumente a frequência!")
        continue
    elif checar_componente == "extremeSmallCapacitor":
        print("Capacitor muito pequeno, aumente a frequência")
        continue
    elif checar_componente == "largeInductor":
        print("Indutor grande, diminua a frequência!")
        continue
    elif checar_componente == "smallInductor":
        print("Indutor pequeno, aumente a frequência!")
        continue
    elif checar_componente == "extremeSmallInductor":
        print("Indutor muito pequeno, aumente a frequência!")
        continue
    elif checar_componente == None:
        print("Não se conseguiu checar o tamanho do componente!")
        continue
    
    #Calcular o valor do componente de acordo com o valor de tau
    valor_calculado = func.get_value(component.type, checar_componente, component.resistor)
    if valor_calculado == None:
        print("Não foi possível calcular o valor do componente!")
        continue
    print_valor_calculado = func.format_number(valor_calculado)
    if print_valor_calculado == "outOfRange":
        print("Formatação do valor calculado fora do range (m, µ, n, p).")
        continue

    if component.type == "capacitor":
        print("Valor do componente: ", print_valor_calculado, end='F\n')
    elif component.type == "inductor":
        print("Valor do componente: ", print_valor_calculado, end='H\n')

    plt.plot(new_time, new_V_source)
    plt.plot(new_time, new_V_component)
    plt.show()


import ltspice
import csv
import numpy as np


class Capacitor_Indutor:
    def __init__(self, origin, resistor, V_in, tau):
        self.origin = origin
        self.resistor = resistor
        self.V_in = V_in
        self.tau = tau
        self.type = None

    def simulator(self):

        filename = 'ltspice/ltspice_simulation.raw'
        try:
            l = ltspice.Ltspice(filename)
        except:
            print(f'Caminho {filename} não encontrado. Verifique o caminho ou pasta!')
        else:
            l.parse()

            self.time = l.get_time()
            self.V_source = l.get_data('V(source)')
            self.V_component = l.get_data('V(component)')

    def oscilloscope(self):
        
        filename = 'oscilloscope/data.csv'
        try:
            with open(filename, 'r') as f:
                csvreader = csv.reader(f)
                csv_list = [list(filter(lambda x: x != '', row)) for row in csvreader]
        except FileNotFoundError:
            print(f'Arquivo {filename} não encontrado. Verifique o nome ou diretório atual.')

        time = []
        v_source = []
        v_component = []

        for row in csv_list[17:]:
            time.append(float(row[0]))
            v_source.append(float(row[1]))
            v_component.append(float(row[3]))  
        
        deslocamento = abs(time[0])
        
        if time[0] < 0:
            self.time = np.array([value + deslocamento for value in time])
        if time[0] > 0:
            self.time = np.array([value - deslocamento for value in time])
        
        self.V_source = np.array(v_source)
        self.V_component = np.array(v_component)

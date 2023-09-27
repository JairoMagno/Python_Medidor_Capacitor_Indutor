import ltspice

class Capacitor_Indutor:
    def __init__(self, origin, resistor, V_in, tau):
        self.origin = origin
        self.resistor = resistor
        self.V_in = V_in
        self.tau = tau
        self.type = None

    def simulator(self):

        filename = 'ltspice/ltspice_simulation.raw'
        l = ltspice.Ltspice(filename)
        l.parse()

        self.time = l.get_time()
        self.V_source = l.get_data('V(source)')
        self.V_component = l.get_data('V(component)')

    def oscilloscope(self):
        pass
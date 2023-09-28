from class_component import Capacitor_Indutor

test = Capacitor_Indutor(origin='oscilloscope', resistor=39_000, V_in=5, tau=4)
test.oscilloscope()
dorimen = Capacitor_Indutor(origin='simulator', resistor=39_000, V_in=5, tau=4)
dorimen.simulator()
print(test.V_source)
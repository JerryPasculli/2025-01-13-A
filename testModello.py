from model.model import Model

self_model = Model()
t1 = self_model.creaGrafo("cytoplasm")
print(t1)
t2 = self_model.dettagli()
print(t2)
t3 = self_model.setMinimo()
print(t3)
import networkx as nx
from network_diffusion.multiplex_network import MultiplexNetwork
from network_diffusion.propagation_model import PropagationModel
from network_diffusion.multi_spreading import MultiSpreading

# initialise multiplex network
layers = [nx.les_miserables_graph(), nx.les_miserables_graph(), nx.les_miserables_graph()]
names = ['illness', 'awareness', 'vaccination']
network = MultiplexNetwork()
network.load_layers_nx(layers, names)
network.describe()

# initialise propagation model and set possible transitions with probabilities
model = PropagationModel()
phenomenas = [('S', 'I', 'R'), ('UA', 'A'), ('UV', 'V')]
for l, p in zip(names, phenomenas):
    model.add(l, p)
model.compile()

model.set_transition('illness.S', 'illness.I', ('vaccination.UV', 'awareness.UA'), 0.3)
model.set_transition('illness.S', 'illness.I', ('vaccination.V', 'awareness.A'), 0.05)
model.set_transition('illness.S', 'illness.I', ('vaccination.UV', 'awareness.A'), 0.1)
model.set_transition('illness.I', 'illness.R', ('vaccination.UV', 'awareness.UA'), 0.01)
model.set_transition('illness.I', 'illness.R', ('vaccination.V', 'awareness.A'), 0.9)
model.set_transition('illness.I', 'illness.R', ('vaccination.UV', 'awareness.A'), 0.05)


model.set_transition('vaccination.UV', 'vaccination.V', ('awareness.A', 'illness.S'), 0.2)
model.set_transition('vaccination.UV', 'vaccination.V', ('awareness.A', 'illness.I'), 0.8)

model.set_transition('awareness.UA', 'awareness.A', ('vaccination.UV', 'illness.S'), 0.3)
model.set_transition('awareness.UA', 'awareness.A', ('vaccination.V', 'illness.S'), 1)
model.set_transition('awareness.UA', 'awareness.A', ('vaccination.UV', 'illness.I'), 0.5)
model.describe()

# initialise starting parameters of propagation in network
phenomenas = {'illness': (70, 6, 1), 'awareness': (60, 17), 'vaccination': (70, 7)}

# perform propagation experiment
experiment = MultiSpreading(model, network)
experiment.set_initial_states(phenomenas)
# experiment._network.describe()
logs = experiment.perform_propagation(10)
# experiment._network.describe()

# plot out experiment results
logs.plot()
import nexusformat.nexus as nx
f = nx.nxload("model.50-3.31.hdf5")
print(f.tree)

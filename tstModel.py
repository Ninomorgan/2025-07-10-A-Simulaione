from model.model import Model

mymodel = Model()

mymodel.creaGrafo("Electric Bikes", "2016-01-01", "2018-12-28")

n, m = mymodel.getGrafoDetails()
print(f"Grafo creato: {n} nodi, {m} archi")

for u, v in mymodel._grafo.edges:
    peso = mymodel._grafo[u][v]["weight"]
    print(f"{u} -> {v} | peso: {peso}")
    break

nodo = list(mymodel._grafo.nodes)[0]

print("Nodo:", nodo)

print("Archi uscenti:")
for u, v in mymodel._grafo.out_edges(nodo):
    print(f"{u} -> {v} | peso {mymodel._grafo[u][v]['weight']}")

print("Archi entranti:")
for u, v in mymodel._grafo.in_edges(nodo):
    print(f"{u} -> {v} | peso {mymodel._grafo[u][v]['weight']}")
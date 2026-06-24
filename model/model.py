import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
      #  self._grafo = nx.Graph()  # grafo semplice non diretto

        self._grafo = nx.DiGraph() #grafo diretto

        self._products=[] #lista nodi
        self._idMapVendite={}

        self._bestCammino = []
        self._bestScore = 0

    def getDateRange(self):
        return DAO.getDateRange()

    def getAllCategory(self): #2 aggiungere da dao a model - ora mettre su controller
        return DAO.getAllCategory()

    def getAllProduct(self, category):
        return DAO.getAllProduct(category)

    def creaGrafo(self, category, startDate,endDate):

        self._grafo.clear()

        #agggiungiamo nodi
        self._products=self.getAllProduct(category)
        self._grafo.add_nodes_from(self._products)

        #mappa venditr
        self._idMapVendite=DAO.getVenditeProdotto(category, startDate, endDate)

       #archi diretti pesat
        for p1, p2 in itertools.combinations(self._products, 2):

            vendite1 = self._idMapVendite.get(p1.product_id, 0)
            vendite2 = self._idMapVendite.get(p2.product_id, 0)

            peso = vendite1 + vendite2

            if vendite1 > vendite2: #da 1- a 2
                self._grafo.add_edge(p1, p2, weight=peso)

            elif vendite2 > vendite1: #da 2 a 1
                self._grafo.add_edge(p2, p1, weight=peso)

            else: #entrambi uguale
                self._grafo.add_edge(p1, p2, weight=peso)
                self._grafo.add_edge(p2, p1, weight=peso)


    def getGrafoDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def _getVenditeProdotto(self, category, startDate, endDate):
        return DAO.getVenditeProdotto(category, startDate, endDate)

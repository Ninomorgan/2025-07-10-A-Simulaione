import copy
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

            if vendite1 == 0 or vendite2 == 0:
                continue

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

    def _getBestProdotti(self):

            result = []
            for p in self._grafo.nodes:
                totUscenti = 0
                totEntranti = 0
                score = 0
                for o,d in self._grafo.in_edges(p): #origine , destinazione
                    peso= self._grafo[o][d]['weight']
                    totEntranti+=peso

                for o,d in self._grafo.out_edges(p):
                    peso = self._grafo[o][d]['weight']
                    totUscenti += peso

                score = totUscenti-totEntranti
                result.append((p, score))

            result.sort(key=lambda x: x[1], reverse=True)

            return result[:5]

    def getNodi(self):
        return self._grafo.nodes()

    def getPesoArco(self, v1, v2):
        return self._grafo[v1][v2]["weight"]

    #RICORDIONE CAMMINO oTTIMO

    #copppia metodi RICORISONE
    def getPath(self, p, a, LMax): #partenza, arrivo, lunghezza max
        self._bestCammino = []
        self._bestScore = 0

        parziale = [p]

        #ripeto in ricoscrione

        self._ricorsione(parziale, a,LMax)
        parziale.pop()
        return self._bestCammino, self._bestScore

    def _ricorsione(self,parziale, a,LMax):

        #1) parziale uguale best score  e terminmo
        if parziale[-1] == a: #condizione che mi fa terminare
            if self._score(parziale) >self._bestScore:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._score(parziale)
            return

        #2) condizione terminazione MAX LUNGHEZZA

        if len(parziale) -1 == LMax:
            return

        #3)RICORSIONE
        for v in self._grafo.successors(parziale[-1]): #CON DIgrag SI GUARDANO I SUCCESSORI

            if v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale, a, LMax)
                parziale.pop()


    def _score(self, parziale): #UGUALE

        #arrivano nodi e preso il parziale e quellodopo prende il peso e lo somma a score
        score= 0
        for i in range (0 , len(parziale)-1):
            score+= self._grafo[parziale[i]][parziale[i+1]]["weight"]

        return score









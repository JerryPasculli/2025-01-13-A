import copy
import networkx as nx
from networkx.classes import subgraph

from database.DAO import DAO

class Model:
    def __init__(self):
        self._G = nx.Graph()
        self._nodi = []
        self._archi = []
        self._Dnodi = []


    def getLocal(self):
        return DAO.get_local()


    def creaGrafo(self, tipo):
        self._G = nx.Graph()
        self._nodi = DAO.get_nodi(tipo)
        self._archi = DAO.get_archi(tipo)
        self._Dnodi = {}
        self._G.add_nodes_from(self._nodi)
        for element in self._nodi:
            self._Dnodi[element._GeneId] = element
        for element in self._archi:
            nodo1 = self._Dnodi[element[0]]
            nodo2 = self._Dnodi[element[1]]
            peso = element[2]
            self._G.add_edge(nodo1, nodo2, weight = peso)
        stringa = f"Grafo creato con {self._G.number_of_nodes()} nodi e {self._G.number_of_edges()} archi."
        for element in self._archi:
            stringa = stringa + f"\n{element[0]}<-->{element[1]}: peso {str(element[2])}"
        return stringa

    def dettagli(self):
        listina = sorted(nx.connected_components(self._G), key = len, reverse=True)
        stringhetta =""
        self._nodi.sort()
        for element in listina:
            grafo = self._G.subgraph(element)
            if grafo.number_of_nodes()>1:
                stringa = ""
                for nodo in grafo.nodes():
                    if stringa != "":
                        stringa = stringa + f",{nodo._GeneId}"
                    else:
                        stringa = stringa + f"{nodo._GeneId}"
                stringa = stringa + f"| dimensione componente = {grafo.number_of_nodes()}"
            if stringhetta == "":
                stringhetta = stringa
            else:
                stringhetta = stringhetta + "\n" + stringa
        stringhetta = "Le componenti connesse sono:\n" + stringhetta
        return stringhetta


    def setMinimo(self):
        self._soluzione = []
        self._tot = 0
        self._tutti = []
        self._flag = ""
        lista = []
        lista1 = []
        for element in self._nodi:
            flag = element._Essential
            if flag == "Essential":
                lista.append(element)
            if flag == "Non-Essential":
                lista1.append(element)
        if len(lista)>len(lista1):
            self._tutti = copy.deepcopy(lista)
            self._flag = "Essential"
        if len(lista1)>len(lista):
            self._tutti = copy.deepcopy(lista1)
            self._flag = "Non-Essential"
        if len(lista1) == len(lista):
            if nx.number_connected_components(self._G.subgraph(lista))<nx.number_connected_components(self._G.subgraph(lista1)):
                self._tutti = copy.deepcopy(lista)
                self._flag = "Essential"
            if nx.number_connected_components(self._G.subgraph(lista1)) < nx.number_connected_components(
                    self._G.subgraph(lista)):
                self._tutti = copy.deepcopy(lista1)
                self._flag = "Non-Essential"
        self._GG = self._G.subgraph(self._tutti)
        for element in self._tutti:
            parziale = [element]
            self.itera(parziale, element, 0)
        stringa = f"Percorso massimo di lunghezza: {self._tot}, e flag:{self._flag}"
        for element in self._soluzione:
            stringa = stringa +f"\n{element._GeneId} - {element._Essential}"
        return stringa

    def itera(self, parziale, partenza, tot):
        if tot>self._tot:
            self._tot = len(parziale)
            self._soluzione = copy.deepcopy(parziale)
        for element in self._GG.neighbors(partenza):
            if element not in parziale:
                parziale.append(element)
                tot1 = self._GG[partenza][element]["weight"] + tot
                self.itera(parziale, element, tot1)
                parziale.pop()


class Nodo:
    def __init__(self, GeneID, Essential):
        self._GeneId = GeneID
        self._Essential = Essential

    def __hash__(self):
        return hash(self._GeneId)

    def __eq__(self, other):
        if other is None:
            return False
        return self._GeneId==other._GeneId

    def __lt__(self, other):
        return self._GeneId<other._GeneId
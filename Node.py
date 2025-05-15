class Node:
    def __init__(self, atributte, value=None, name=None, isClass=False, counter=0):
        self.atributte = atributte           # Índice do atributo ou valor da classe
        self.value = value                  # Valor do atributo que leva a este nó
        self.name = name                    # Nome do atributo
        self.isClass = isClass              # True se for um nó folha (classe final)
        self.counter = counter              # Contador de exemplos que chegaram aqui
        self.children = []                  # Lista de filhos (nós seguintes)

    def addNeighbour(self, node):
        self.children.append(node)

    def getNeighbours(self):
        return self.children

    def getAttribute(self):
        return self.atributte

    def getValue(self):
        return self.value

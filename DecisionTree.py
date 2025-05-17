from ID3 import ID3
from Node import Node
from Dataset import Dataset
import copy

class DecisionTree():

    def __init__(self, dataset, binning = False):
        self.initialDataset = dataset
        self.binning = binning
        self.root = self.__generateNode(dataset)

    #Gera a àrvore com nós do tipo node (atributo em número, valor do atributo, atributo em str ) -> está definido em Node.py (tem mais alguns argumentos)
    #explicação:
    #   Com o calculo do ganho de informação, sabemos qual o próximo atributo que explorar (bestAtributte)
    #   Com esse atributo (vamos ver todos os seus valores), vamos ver se há algum valor desse atributo que tenha 100% de probabilidade de ser uma classe
    #   Se for 100% = p(1.0), podemos logo decidir, e criamos uma folha (nó final) 
    #   Caso não seja verificamos se apenas temos um atributo e uma classe, se apenas tivermos, escolhemos a classe com mais probabilidade para o valor do atributo
    #   Se não for nenhum dos 2 ultimos casos, temos que retirar os valores do atributo que não estamos a explorar, e fazer chamada recursiva dessa cópia do dataset sem as linhas dos valores do atributo a não serem explorados

    def __generateNode(self, dataset, tabI=0, numRemovedColumns=0, value=None):
        attribute, values = ID3(dataset).bestAtributte
        node = Node(attribute, value, dataset.header[attribute])

        #A partida nenhum é classe 
        for key in values:
            isClass = False
            maxValue = float('-inf')
            maxkey = 'failed'
            maxkey2 = 'failed'

            #Particularudades (100% de ser classe, ou apenas termos um atributo e uma classe)
            for key2 in values[key]:
                if (key2 != "total"):
                    #Probabilidade 100% ser essa classe (vira folha)
                    #caso base
                    if (values[key][key2] == 1.0):
                        node.addNeighbour(Node(key2, key, None, True, values[key]["total"]))
                        isClass = True
                        break
                    #caso aja apenas um atributo e uma classe, escolhe a classe mais provavel para cada valor do atributo
                    elif (len(dataset.header) == 2):
                        if maxValue < values[key][key2] :#and key2 != "total":
                            maxValue = values[key][key2]
                            maxkey = key
                            maxkey2 = key2

            #Nós não folha (ainda há caminho para explorar)
            if (not isClass):

                #transforma em nó folha (só tem 1 atributo e 1 classe)
                #adiciona aos vizinhos
                #caso base
                if (len(dataset.header) == 2):
                    node.addNeighbour(Node(maxkey2, maxkey, None, True, int(values[maxkey]["total"]*values[maxkey][maxkey2])))
                #caso aja mais atributos para explorar
                else:
                    
                    #retiramos as linhas dos valores do atributo que não estamos a explorar 
                    datasetCopy = dataset.copy()
                    linestoRemove = []
                    for i in range(len(datasetCopy.array)):
                        if (datasetCopy.array[i][attribute] != key):
                            linestoRemove.append(i)

                    #para não mudar o número das que têm de ser removidas
                    for x in sorted(linestoRemove, reverse=True):
                        datasetCopy.removeLine(x)

                    #retira o atributo visto
                    datasetCopy.removeColumn(attribute)

                    #contrução recursiva, para os próximos valores do atributo    
                    node.addNeighbour(self.__generateNode(datasetCopy, tabI+2, numRemovedColumns+1, key))

        return node

    def DFSPrint(self, tabI=0, node=None):
        if node is None:
            node = self.root

        print('\t' * tabI + '<' + str(node.label) + '>')

        for currentNode in node.getNeighbours():
            if currentNode.isClass:
                print('\t' * (tabI + 1) + str(currentNode.getValue()) + ': ' +
                    str(currentNode.getAttribute()) + ' (' + str(currentNode.counter) + ')')
            else:
                print('\t' * (tabI + 1) + str(currentNode.getValue()) + ':')
                self.DFSPrint(tabI + 2, currentNode)
    
    #------------------------------------------------------

    def classifyMultipleExamples(self, path, file):

        dataset = Dataset().readCSV(path, file, True, False)
        for line in range(dataset.lines):
            classExmp = self.classifyExample(copy.deepcopy(dataset), line)
            if (classExmp == -1):
                print('Not Found!!')
            else:
                print('Line ' + str(line+1) + ' Class: ' + classExmp)
        return



    #Percorre a árvore à procura de um nó folha, tenta ver o caminho do valor do atributo a que corresponde
    def classifyExample(self, dataset, line):
        #nó atual
        actualNode = self.root
        #valor do atributo que estamos a ver
        value = dataset.array[line][actualNode.getAttribute()]

        #Enquanto não é folha 
        while not actualNode.isClass:
            neighbours = actualNode.getNeighbours()
            found = False

            #ver nós vizinhos
            for node in neighbours:

                #valor do atributo
                node_val = node.getValue()

                #caso de não usar binning
                if not self.binning:
                    if node_val == value:
                        #retira a coluna do atributo que está a explorar, pois já encontrou um nó com o mesmo valor de atributo nesse mesmo atributo
                        dataset.removeColumn(actualNode.getAttribute())
                        #vizinho é o nó a explorar
                        actualNode = node

                        #se o vizinho escolhido, não for folha, o valor do atributo de outra coluna (pois já eliminamos a que estavamos a ver)
                        if not actualNode.isClass:
                            value = dataset.array[line][actualNode.getAttribute()]
                        
                        #caso de haver um node_val == value (temos caminho)
                        found = True
                        break
                #caso de usar binning no dataset    
                else:
                    
                    if '-' in node_val:
                        try:
                            minVal, maxVal = map(float, node_val.split('-'))
                            
                            if '-' in str(value):
                                vmin, vmax = map(float, value.split('-'))
                                val = (vmin + vmax) / 2
                            else:
                                val = float(value)
                        except:
                            continue

                        if minVal <= val <= maxVal:
                            dataset.removeColumn(actualNode.getAttribute())
                            actualNode = node
                            if not actualNode.isClass:
                                value = dataset.array[line][actualNode.getAttribute()]
                            found = True
                            break
                    else:
                        
                        if node_val == value:
                            dataset.removeColumn(actualNode.getAttribute())
                            actualNode = node
                            if not actualNode.isClass:
                                value = dataset.array[line][actualNode.getAttribute()]
                            found = True
                            break
            #Não há caminho para o exemplo a ver
            if not found:
                return -1
        #Resultado da classe
        return actualNode.getAttribute()

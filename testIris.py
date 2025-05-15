from Dataset import Dataset
from DecisionTree import DecisionTree
from copy import deepcopy

#Lê o dataset com binning aplicado antes da divisão
dataset = Dataset().readCSV('./datasets/', 'iris', hasId=False, hasHeader=True, binCount=3)

#Divide em treino e teste (90% treino, 10% teste)
split_point = int(0.9 * dataset.lines)
train_data = Dataset(deepcopy(dataset.array[:split_point]), deepcopy(dataset.header))
test_data = Dataset(deepcopy(dataset.array[split_point:]), deepcopy(dataset.header))

#Cria a árvore com o dataset de treino
tree = DecisionTree(train_data, binning=True)
print("\n Árvore de Decisão\n")
tree.DFSPrint()
print('\nAvaliação no conjunto de teste:\n')

#Testa linha a linha
acertos = 0
total = test_data.lines

for i in range(total):
    previsto = tree.classifyExample(deepcopy(test_data), i)
    real = test_data.getValue(i, test_data.cols - 1)
    print(f"Linha {i+1}: Previsto = {previsto} | Real = {real}")
    if previsto == real:
        acertos += 1

print(f"\nPrecisão do conjunto de teste: {acertos}/{total} = {acertos/total*100:.2f}%")
